from typing import List, Type

from qcodes import Instrument

from quantify_nano.utilities.general import delete_keys_from_dict


def snapshot(update: bool = False, clean: bool = True) -> dict:
    """
    State of all instruments setup as a JSON-compatible dictionary (everything that the
    custom JSON encoder class :class:`qcodes.utils.helpers.NumpyJSONEncoder` supports).

    Parameters
    ----------
    update
        If True, first gets all values before filling the snapshot.
    clean
        If True, removes certain keys from the snapshot to create a more readable and
        compact snapshot.
    """
    snap: dict = {"instruments": {}, "parameters": {}}

    instruments: List[Instrument] = get_all_instances(Instrument)

    for instrument in instruments:
        if instrument is not None:
            ins_name = instrument.name
            snap["instruments"][ins_name] = instrument.snapshot(update=update)

    if clean:
        exclude_keys = {
            "inter_delay",
            "post_delay",
            "vals",
            "instrument",
            "functions",
            "__class__",
            "raw_value",
            "instrument_name",
            "full_name",
            "val_mapping",
        }
        snap = delete_keys_from_dict(snap, exclude_keys)

    return snap


def get_all_instances(cls: Type[Instrument]) -> List[Instrument]:
    """
    Recursively gather all instances of a given class and its subclasses

    Parameters
    ----------
    cls
        The class for which to gather instances
    """
    instances: List[Instrument] = cls.instances()

    subclasses = cls.__subclasses__()

    for subclass in subclasses:
        instances.extend(get_all_instances(subclass))

    return instances
