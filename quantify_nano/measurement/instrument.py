import json
import os

from qcodes import Instrument
from qcodes import validators as vals
from qcodes.instrument.parameter import InstrumentRefParameter, ManualParameter


class MeasurementControl(Instrument):
    def __init__(self, name: str):
        """
        Creates an instance of the Measurement Control.

        Parameters
        ----------
        name
            name of this instrument.
        """
        super().__init__(name=name)

        self.update_interval = ManualParameter(
            initial_value=0.5,
            vals=vals.Numbers(min_value=0.1),
            instrument=self,
            name="update_interval",
        )
        """Interval for updates during the data acquisition loop, every time more than
        :attr:`.update_interval` time has elapsed when acquiring new data points, data
        is written to file (and the live monitoring detects updated)."""


class Device(Instrument):
    """A dummy instrument."""

    def __init__(self, name: str):
        super().__init__(name=name)

        self.add_parameter(name="amp_0", unit="A", parameter_class=ManualParameter)
        self.add_parameter(name="amp_1", unit="A", parameter_class=ManualParameter)
        self.add_parameter(name="offset", unit="A", parameter_class=ManualParameter)
