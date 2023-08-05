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

import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug(f'{__file__} will get logged')


def update_fluid(func):
    def wrapper(self, value):
        func(self, value)
        try:
            self.fluid.update(fld.Input.pressure(self._pressure), fld.Input.temperature(self._temperature))
        except:
            pass

    return wrapper


class Fluid:
    fluid_instances = {
        'Fluid': fld.Fluid,
        # @TODO implement Mixture and Humid Air
        # 'Mixture': fld.Mixture,
        # 'HumidAir': fld.HumidAir
    }

    def __init__(self, title: str, pressure: float = 101325, temperature: float = 293.15, instance: str = 'Fluid'):
        if isinstance(title, fld.Fluid):
            fluid = title
            self.title = fluid.name
            self.fluid = fluid
        else:
            self.instance = instance

            self.title = title
            self.fluid = None
            # setting initial conditions at NTP
            # @TODO could lead to problems with some fluids
            self._pressure = pressure
            self._temperature = temperature

            self.pressure = pressure
            self.temperature = temperature

    @property
    def instance(self):
        return self.__instance

    @instance.setter
    def instance(self, value):
        try:
            self.__instance = self.fluid_instances[value]
        except KeyError:
            raise AttributeError("instance not implemented")

    @property
    def title(self):

        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def fluid(self):
        return self._fluid

    @fluid.setter
    def fluid(self, value=None):
        if isinstance(value, fld.Fluid):
            self._fluid = value
            logging.debug(f'Creating Fluid by fld object\n id = {id(self)}\n Unit system = {self.fluid.units_system}')
        elif value is not None:
            raise NotImplementedError
        else:
            try:
                self._fluid = self.instance(fld.FluidsList[self._title])
                logging.debug(f'Creating Fluid by title\n id = {id(self)}\n Unit system = {self.fluid.units_system}')
            except KeyError:
                raise NotImplementedError("Fluid not implemented. Check spelling")

    @property
    def pressure(self):
        return self.fluid.pressure

    @pressure.setter
    def pressure(self, value):
        try:
            self.fluid.update(fld.Input.pressure(value), fld.Input.temperature(self._temperature))
            self._pressure = value
            logging.debug("setting pressure")
        except AttributeError:
            logging.debug("pressure not yet defined")
        except ValueError as e:
            logging.debug(f"resetting pressure to {self._pressure}\n {e}")
            self.fluid.update(fld.Input.pressure(self._pressure), fld.Input.temperature(self._temperature))
            print(f"pressure not supported, please change pressure\n {e}")

    @property
    def temperature(self):
        return self.fluid.temperature

    @temperature.setter
    def temperature(self, value):
        try:
            self.fluid.update(fld.Input.pressure(self._pressure), fld.Input.temperature(value))
            self._temperature = value
            logging.debug("setting temperature")
        except AttributeError:
            logging.debug("temperature not yet defined")
        except ValueError as e:
            logging.debug(f"resetting temperature to {self._temperature}\n {e}")
            self.fluid.update(fld.Input.pressure(self._pressure), fld.Input.temperature(self._temperature))
            print(f"Temperature not supported, please change temperature\n {e}")

    @property
    def specific_heat(self):
        return self.fluid.specific_heat

    def clone(self):
        new_fluid = Fluid(self.fluid)
        return new_fluid

    def __repr__(self):
        output = f"Fluid: title = {self.title} id = {id(self)}\n"
        output += f"\tp = {self.pressure} Pa\n" \
                  f"\tt = {self.temperature - 273.15} °C"
        return output

    """


    def _set_fluid(self):
        try:
            fluid = fld.Fluid(fld.FluidsList[self._title])
        except KeyError:
            raise NotImplementedError("Fluid not implemented. Check spelling")
        fluid = fluid.with_state(fld.Input.pressure(self._pressure),
                                 fld.Input.temperature(self._temperature))
        
        #if fluid.phase.name == 'Gas':
        #    raise NotImplementedError("phase = Gas is not implemented")
        return fluid

    def get_specific_heat(self):
        return self._fluid.specific_heat

    def factory(self):
        # create new fluid object at NTP (normal temperature and pressure)
        return Fluid(self._title)

    def with_state(self):
        # clones fluid object
        return Fluid(self.title, self.pressure, self.temperature)

    def __repr__(self):
        try:
            str_fluid = str(self._fluid.as_dict())
        except:
            str_fluid = "state not yet defined"
        return str_fluid

    """


class Flow:
    def __init__(self, fluid: Fluid = None, mass_flow=None):
        self._in_fluid = fluid
        self._out_fluid = self._set_out_fluid()
        self._mean_fluid = self._in_fluid.factory()
        self._mass_flow = mass_flow

    @property
    def id(self):
        return id(self)

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
        # f = self._in_fluid.factory()
        f = self._in_fluid.with_state()
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
        # return self.mean_fluid.get_specific_heat() * self.mass_flow*(self.in_fluid.temperature-self.out_fluid.temperature)
        return self.mass_flow * self.mean_fluid.get_specific_heat()

    def str_heat_capacity_flow(self):
        return f"Wärmekapazitätsstrom: W_dot = %.2f W/K\n" % (self.heat_capacity_flow)

    @property
    def heat_flow(self):
        return self.mass_flow * (self.in_fluid.fluid.enthalpy - self.out_fluid.fluid.enthalpy)

    def str_heat_flow(self):
        return f"Wärmestrom: Q_dot = %.2f W\n" % (self.heat_flow)

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

    def copy(self):
        fluid = Fluid(self.in_fluid.title, self.in_fluid.pressure, self.in_fluid.temperature)
        return Flow(fluid, self.mass_flow)

    @staticmethod
    def deserialize(data):
        flow = Flow(Fluid(data["fluid"], data["pressure"], data["temperature"]), data["mass_flow"])
        return flow


if __name__ == "__main__":
    """
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
    """
    fluid_in = Fluid("Water", temperature=273.15 + 100)
    flow = Flow(fluid_in, 1)
    flow.out_fluid.temperature = 273.15 + 99
    print(flow)
    print(flow.str_heat_capacity_flow())
    print(flow.str_heat_flow())
