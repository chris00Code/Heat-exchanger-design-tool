import copy
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

logging.basicConfig(level=logging.CRITICAL)
logging.debug(f'{__file__} will get logged')


class Fluid:
    fluid_instances = {
        'Fluid': fld.Fluid,
        # @TODO implement Mixture and Humid Air
        # 'Mixture': fld.Mixture,
        # 'HumidAir': fld.HumidAir
    }

    def __init__(self, title: str, pressure: float = 101325, temperature: float = 293.15, instance: str = 'Fluid'):
        if isinstance(title, fld.Fluid):
            fluid = title.clone()
            self.title = fluid.name
            self.fluid = fluid

        else:
            self.instance = instance

            self.title = title
            self.fluid = None

            self.ntp_state()
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
        prev_pressure = self.fluid.pressure
        temp = self.fluid.temperature
        try:
            self.fluid.update(fld.Input.pressure(value), fld.Input.temperature(temp))
            logging.debug("setting pressure")
        except AttributeError:
            logging.debug("pressure not yet defined")
        except ValueError as e:
            logging.debug(f"resetting pressure to {prev_pressure}\n {e}")
            self.fluid.update(fld.Input.pressure(prev_pressure), fld.Input.temperature(temp))
            print(f"pressure not supported, please change pressure\n {e}")

    @property
    def temperature(self):
        return self.fluid.temperature

    @temperature.setter
    def temperature(self, value):
        pressure = self.fluid.pressure
        prev_temp = self.fluid.temperature
        try:
            self.fluid.update(fld.Input.pressure(pressure), fld.Input.temperature(value))
            logging.debug("setting temperature")
        except AttributeError:
            logging.debug("temperature not yet defined")
        except ValueError as e:
            logging.debug(f"resetting temperature to {prev_temp}\n {e}")
            self.fluid.update(fld.Input.pressure(pressure), fld.Input.temperature(prev_temp))
            print(f"Temperature not supported, please change temperature\n {e}")

    def ntp_state(self):
        self.fluid.update(fld.Input.pressure(101325), fld.Input.temperature(293.15))

    @property
    def specific_heat(self):
        return self.fluid.specific_heat

    @property
    def density(self):
        return self.fluid.density

    def clone(self):
        new_fluid = Fluid(self.fluid)
        return new_fluid

    def __repr__(self):
        output = f"Fluid: title = {self.title}, id = {id(self)}\n"
        output += f"\tp = {self.pressure} Pa\n" \
                  f"\tt = {self.temperature - 273.15} °C"
        return output


class Flow:
    def __init__(self, fluid: Fluid = None, mass_flow: float = None, volume_flow: float = None):
        if isinstance(fluid, Flow):
            flow = fluid
            self.in_fluid = flow.in_fluid.clone()
            self.out_fluid = flow.out_fluid.clone()
            self.volume_flow = flow.volume_flow
        else:
            self.in_fluid = fluid
            self.out_fluid = None
            if mass_flow is not None and volume_flow is not None:
                raise NotImplementedError("Only implement one flow rate")
            elif volume_flow is not None:
                self.volume_flow = volume_flow
            elif mass_flow is not None:
                self.mass_flow = mass_flow

    @property
    def in_fluid(self):
        return self._in_fluid

    @in_fluid.setter
    def in_fluid(self, value):
        self._in_fluid = value

    @property
    def out_fluid(self):
        return self._out_fluid

    @out_fluid.setter
    def out_fluid(self, value):
        if value is None:
            self._out_fluid = self.in_fluid.clone()
        elif isinstance(value,Fluid):
            self._out_fluid = value

    @property
    def mean_fluid(self):
        mean_temp = sum([self.in_fluid.temperature, self.out_fluid.temperature]) / 2
        mean_pressure = sum([self.in_fluid.pressure, self.out_fluid.pressure]) / 2
        fluid = Fluid(str(self.in_fluid.title), pressure=mean_pressure, temperature=mean_temp)
        return fluid

    @property
    def volume_flow(self):
        "an incompressible flow is assumed"
        return self._volume_flow

    @volume_flow.setter
    def volume_flow(self, value):
        self._volume_flow = value

    @property
    def pressure_loss(self):
        return self.in_fluid.pressure - self.out_fluid.pressure

    @pressure_loss.setter
    def pressure_loss(self, value):
        out_pressure = self.in_fluid.pressure - value
        self.out_fluid.pressure = out_pressure
        logging.debug(f"setting pressure loss {value} Pa, new out pressure = {out_pressure}")

    @property
    def out_temperature(self):
        return self.out_fluid.temperature

    @out_temperature.setter
    def out_temperature(self, value):
        self.out_fluid.temperature = value
        if self.phase_change:
            raise Warning("the phase changes, this could lead to some problems")

    @property
    def phase_change(self) -> bool:
        return self.in_fluid.fluid.phase != self.out_fluid.fluid.phase

    @property
    def mass_flow(self):
        value = self.volume_flow * self.mean_fluid.density
        return value

    @mass_flow.setter
    def mass_flow(self, value):
        self._volume_flow = value / self.mean_fluid.density

    def mass_flow_str(self):
        return f"mass flow = %.5f kg/s" % self.mass_flow

    @property
    def heat_capacity_flow(self):
        return self.mass_flow * self.mean_fluid.specific_heat

    def heat_capacity_flow_str(self):
        return f"heat capacity flow: W_dot = %.5f W/K" % (self.heat_capacity_flow)

    @property
    def heat_flow(self):
        if self.phase_change:
            raise Warning("the phase changes, this could lead to some problems")
        heat_flow_enthalpy = self.mass_flow * (self.in_fluid.fluid.enthalpy - self.out_fluid.fluid.enthalpy)
        # heat_flow_temps = self.heat_capacity_flow * (self.in_fluid.temperature - self.out_fluid.temperature)
        return heat_flow_enthalpy

    def heat_flow_str(self):
        return f"heat flow: Q_dot = %.5f kW\n" % (self.heat_flow * 1e-3)

    def clone(self):
        new_flow = Flow(self)
        return new_flow

    def __repr__(self):
        output = f"Flow: id = {id(self)}\n"
        output += f"\t" + self.mass_flow_str() + "\n"
        output += f"\t" + self.heat_capacity_flow_str() + "\n"
        output += f"\t" + self.heat_flow_str() + "\n"
        output += f"Input Fluid:\n\t{self.in_fluid}\n"
        output += f"Output Fluid:\n\t{self.out_fluid}\n"
        return output

