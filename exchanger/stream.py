import json
import os

"""file_path = os.path.join(os.path.dirname(__file__), "pyfluids.json")
#os.chdir(os.path.dirname(file_path))
#package_path = os.path.dirname(os.path.abspath(__file__))
#file_path = os.path.join(package_path, 'pyfluids.json')

with open(file_path) as config_file:
    config_data = json.load(config_file)
"""
import pyfluids as fld


def update_fluid(func):
    def wrapper(self, value):
        func(self, value)
        self._fluid.update(fld.Input.pressure(self._pressure), fld.Input.temperature(self._temperature))

    return wrapper


class Fluid:
    def __init__(self, title: str, pressure: float = 101325, temperature: float = 293.15):
        self._title = title
        self._pressure = pressure
        self._temperature = temperature
        self._fluid = self._set_fluid()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self._fluid = self._set_fluid()

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    @update_fluid
    def pressure(self, value):
        self._pressure = value

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    @update_fluid
    def temperature(self, value):
        self._temperature = value

    def _set_fluid(self):
        try:
            fluid = fld.Fluid(fld.FluidsList[self._title])
        except KeyError:
            raise NotImplementedError("Fluid not implemented. Check spelling")
        fluid = fluid.with_state(fld.Input.pressure(self._pressure),
                                 fld.Input.temperature(self._temperature))
        return fluid

    def get_specific_heat(self):
        return self._fluid.specific_heat

    def factory(self):
        # create new fluid object at NTP (normal temperature and pressure)
        return Fluid(self._title)

    def __repr__(self):
        try:
            str_fluid = str(self._fluid.as_dict())
        except:
            str_fluid = "state not yet defined"
        return str_fluid


class Flow:
    def __init__(self, fluid: Fluid = None, mass_flow=None):
        self._in_fluid = fluid
        self._out_fluid = self._set_out_fluid()
        self._mean_fluid = self._in_fluid.factory()
        self._mass_flow = mass_flow

    @property
    def in_fluid(self):
        return self._in_fluid

    @in_fluid.setter
    def in_fluid(self, value):
        self._in_fluid = value

    @property
    def out_fluid(self):
        return self._out_fluid

    # sets the out fluid at NTP state
    def _set_out_fluid(self):
        f = self._in_fluid.factory()
        return f

    @property
    def mass_flow(self):
        return self._mass_flow

    @mass_flow.setter
    def mass_flow(self, value):
        self._mass_flow = value

    def mass_flow_repr(self):
        try:
            return "mass flow: %.2f kg/s" % (self._mass_flow)
        except TypeError:
            return ""

    @property
    def mean_fluid(self):
        self.update_mean_fluid()
        return self._mean_fluid

    def update_mean_fluid(self):
        in_temp, in_p = self.in_fluid.temperature, self._in_fluid.pressure
        out_temp, out_p = self.out_fluid.temperature, self._out_fluid.pressure
        mean_temp, mean_p = (in_temp + out_temp) / 2, (in_p + out_p) / 2
        self._mean_fluid.temperature, self._mean_fluid.pressure = mean_temp, mean_p

    @property
    def heat_capacity_flow(self):
        return self.mean_fluid.get_specific_heat() * self.mass_flow

    def get_heat_capacity_flow(self):
        return self.mean_fluid.get_specific_heat() * self.mass_flow

    def str_heat_capacity_flow(self):
        return f"Wärmekapazitätsstrom: W_dot = %.2f W/K\n" % (self.get_heat_capacity_flow())

    def __repr__(self):
        str_in = str(self.in_fluid)
        str_out = str(self.out_fluid)
        return f"Flow:\nInput: %s \nOutput: %s\n" % (str_in, str_out) + self.mass_flow_repr()

    def serialize(self):
        dict = {"fluid": self.in_fluid.title,
                "pressure": self.in_fluid.pressure,
                "temperature": self.in_fluid.temperature,
                "mass_flow": self.mass_flow}
        return dict

    @staticmethod
    def deserialize(data):
        flow = Flow(Fluid(data["fluid"], data["pressure"], data["temperature"]), data["mass_flow"])
        return flow


if __name__ == "__main__":
    fl = Fluid("Air")
    print(fl.get_specific_heat())
    fl.pressure = 500e3
    print(fl._fluid.temperature)
    print(fl.get_specific_heat())

    flow = Flow(fl, 10)
    flow.in_fluid.temperature = 500
    print(flow)
    mean = flow.mean_fluid

    print(flow.mean_fluid.temperature)
    print(flow.str_heat_capacity_flow())

    ser_flow = flow.serialize()
    flow_2 = Flow.deserialize(ser_flow)
    flow.in_fluid.temperature = 300
    print(flow)
    print(flow_2)
