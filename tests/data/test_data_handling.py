import quantify_nano.data.handling as dh
from quantify_nano.measurement.instrument import MeasurementControl, Device


def test_snapshot():
    empty_snap = dh.snapshot()
    assert empty_snap == {"instruments": {}, "parameters": {}}
    test_MC = MeasurementControl(name="MC")
    test_device = Device(name="DUT")

    test_MC.update_interval(0.77)

    snap = dh.snapshot()

    assert snap["instruments"].keys() == {"MC", "DUT"}
    assert snap["instruments"]["MC"]["parameters"]["update_interval"]["value"] == 0.77

    test_MC.close()
    test_device.close()
