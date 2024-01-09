import warnings
import pyfluids as fld
import logging

# Set up logging level
logging.basicConfig(level=logging.CRITICAL)
logging.debug(f'{__file__} will get logged')


class Fluid:
    """
    Represents a fluid with its thermodynamic properties like pressure and temperature.

    This class serves as an interface to the 'pyfluids' library, allowing to model and manage fluid properties.

    Args:
        title (str): The name of the fluid.
        pressure (float, optional): The pressure in Pascals (Pa). Defaults to 101325 Pa.
        temperature (float, optional): The temperature in Kelvin (K). Defaults to 293.15 K.
        instance (str, optional): The type of fluid instance to create. Defaults to 'Fluid'.

        fluid (Fluid): the fluid to be make a deepcopy of

    Attributes:
        fluid_instances (dict): A dictionary mapping instance names to fluid types from pyfluids.

    Methods:
        ntp_state: Set the fluid properties to standard conditions (NTP).
        clone: Create a new Fluid object by cloning the current one.

    Note:
        - The 'pyfluids' library must be installed to use this class.
        - The 'pyfluids' unit system is initialized in 'pyfluids.json' to the International System of Units (SI).
    """

    fluid_instances = {
        'Fluid': fld.Fluid,
        # @TODO implement Mixture and Humid Air
        # 'Mixture': fld.Mixture,
        # 'HumidAir': fld.HumidAir
    }

    def __init__(self, title: str = None, pressure: float = 101325, temperature: float = 293.15,
                 instance: str = 'Fluid',
                 **kwargs):
        if "fluid" in kwargs:
            fluid = kwargs["fluid"]
            if isinstance(fluid, Fluid):
                self.title = fluid.title
                self.fluid = fluid.fluid.clone()
            else:
                raise ValueError("fluid is not a Fluid object")
        else:

            self.instance = instance
            if title is None:
                raise TypeError
            self.title = title
            self.fluid = None

            self.ntp_state()
            self.pressure = pressure
            self.temperature = temperature

    @property
    def instance(self):
        """
        Get or set the type of fluid instance to create.

        If setting a new instance type, it should be one of the supported fluid instances.

        Raises:
            AttributeError: If the provided instance is not implemented.

        Returns:
            instance of pyfluids: The current instance type.
        """
        return self.__instance

    @instance.setter
    def instance(self, value):
        try:
            self.__instance = self.fluid_instances[value]
        except KeyError:
            raise AttributeError(f"instance '{value}' not implemented")

    @property
    def title(self):
        """
        Get or set the title (name) of the fluid.

        Returns:
            str: The current title (name) of the fluid.
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def fluid(self):
        """
        Get or set the fluid object associated with this instance.

        This property represents the fluid's properties and behavior and allows for retrieval and modification of the fluid.

        Setting the fluid can be done in two ways:
        1. By providing an existing 'pyfluids.Fluid' object.
        2. By specifying the fluid's title (name), in which case a new fluid object is created based on the title.

        Args:
            value (pyfluids.Fluid or None, optional): The fluid object to set or None to clear the fluid.

        Raises:
            NotImplementedError: If the provided value is not a valid 'pyfluids.Fluid' object
            or if the fluid title is not implemented in pyfluids.

        Returns:
            pyfluids instance: The current fluid object associated with this instance.
        """
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
        """
        Get or set the pressure of the fluid in Pascals (Pa).

        Args:
            value (float): The new pressure to set in Pascals (Pa).

        Raises:
            ValueError: If the provided pressure value is not valid.

        Returns:
            float: The pressure of the fluid in Pascals (Pa).
        """
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
        """
        Get or set the temperature of the fluid in Kelvin (K).

        Args:
            value (float): The new temperature to set in Kelvin (K).

        Raises:
            ValueError: If the provided temperature value is not valid.

        Returns:
            float: The temperature of the fluid in Kelvin.
        """
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
        """
        Set the fluid properties to standard conditions (NTP - Normal Temperature and Pressure).

        This method updates the fluid's pressure to 101325 Pascals (Pa) and temperature to 293.15 Kelvin (K),
        which are the standard conditions for many fluid properties.
        """
        self.fluid.update(fld.Input.pressure(101325), fld.Input.temperature(293.15))

    @property
    def specific_heat(self):
        """
        Mass specific heat [J/kg/K].

        Returns:
            float: The mass specific heat of the fluid in J/kg/K.
        """
        return self.fluid.specific_heat

    @property
    def density(self):
        """
        Mass density [kg/m3].

        Returns:
            float: The mass density of the fluid in kg/m3.
        """
        return self.fluid.density

    def clone(self):
        """
        Create a new fluid object with the same properties as the current fluid instance.

        Returns:
            Fluid: A new fluid object with identical properties.
        """
        new_fluid = Fluid(fluid=self)
        return new_fluid

    def __repr__(self):
        output = f"Fluid: title = {self.title}, id = {id(self)}\n"
        output += f"\tp = {self.pressure} Pa\n" \
                  f"\tt = {self.temperature - 273.15} °C"
        return output


class Flow:
    """
        Represents a fluid flow with input and output fluids, mass and volume flow rates, and thermodynamic properties.

        This class allows you to model and manage fluid flows and calculate properties such as mass flow rate, heat capacity flow,
        heat flow, and pressure loss. It also handles incompressible flows and phase changes.

        Args:
            fluid (Fluid, optional): The input fluid. Defaults to None.
            mass_flow (float, optional): The mass flow rate in kg/s. Defaults to None.
            volume_flow (float, optional): The volume flow rate in m^3/s. Defaults to None.

        Attributes:
            in_fluid (Fluid): The input fluid.
            out_fluid (Fluid): The output fluid.
            volume_flow (float): The volume flow rate in m^3/s.
            pressure_loss (float): The pressure loss in Pascals (Pa).
            out_temperature (float): The output temperature in Kelvin (K).
            phase_change (bool): Indicates if a phase change occurs in the flow.
            mass_flow (float): The mass flow rate in kg/s.
            heat_capacity_flow (float): The heat capacity flow rate in Watts per Kelvin (W/K).
            heat_flow (float): The heat flow rate in Watts (W).

        Methods:
            mass_flow_str(): Returns a formatted string for mass flow rate.
            heat_capacity_flow_str(): Returns a formatted string for heat capacity flow rate.
            heat_flow_str(): Returns a formatted string for heat flow rate.
            clone(): Creates a new Flow object with the same properties.
            clone_by_fluid(clone_fluid='in'): Creates a new Flow object by cloning and using the specified input or output fluid.

        Note:
            - This class assumes incompressible flow.
            - Warning: Phase changes in the flow may lead to issues.

        """

    def __init__(self, fluid: Fluid = None, mass_flow: float = None, volume_flow: float = None, **kwargs):
        """
        Initialize a Flow object with input fluid, mass flow rate, or volume flow rate.

        Args:
            fluid (Fluid, optional): The input fluid. Defaults to None.
            mass_flow (float, optional): The mass flow rate in kg/s. Defaults to None.
            volume_flow (float, optional): The volume flow rate in m^3/s. Defaults to None.

        Raises:
            NotImplementedError: If both mass_flow and volume_flow are provided.

        """
        if "flow" in kwargs:
            flow = kwargs["flow"]
            if isinstance(flow, Flow):
                self.in_fluid = flow.in_fluid.clone()
                self.out_fluid = flow.out_fluid.clone()
                self.volume_flow = flow.volume_flow
            else:
                raise ValueError("flow is not a Flow object")
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
        """
        Get or set the input fluid of the flow.

        Args:
            value (Fluid): The input fluid.

        Returns:
            Fluid: The input fluid.

        """
        return self._in_fluid

    @in_fluid.setter
    def in_fluid(self, value):
        self._in_fluid = value

    @property
    def out_fluid(self):
        """
        Get or set the output fluid of the flow.

        If the output fluid is not set, it defaults to a copy of the input fluid.

         Args:
            value (Fluid or None): The output fluid or None to reset to a copy of the input fluid.

        Returns:
            Fluid: The output fluid.

        """
        return self._out_fluid

    @out_fluid.setter
    def out_fluid(self, value):
        if value is None:
            self._out_fluid = self.in_fluid.clone()
        elif isinstance(value, Fluid):
            self._out_fluid = value

    @property
    def mean_fluid(self):
        """
        Calculate and return the mean fluid based on the average temperature and pressure between input and output fluids.

        Returns:
            Fluid: The mean fluid with averaged temperature and pressure.

        """
        mean_temp = sum([self.in_fluid.temperature, self.out_fluid.temperature]) / 2
        mean_pressure = sum([self.in_fluid.pressure, self.out_fluid.pressure]) / 2
        fluid = Fluid(str(self.in_fluid.title), pressure=mean_pressure, temperature=mean_temp)
        return fluid

    @property
    def volume_flow(self):
        """
        Get or set the volume flow rate for the incompressible flow.

        Args:
            value (float): The volume flow rate in m^3/s.

        Returns:
            float: The volume flow rate in m^3/s.

        """
        return self._volume_flow

    @volume_flow.setter
    def volume_flow(self, value):
        self._volume_flow = value

    @property
    def pressure_loss(self):
        """
        Calculate and return the pressure loss between input and output fluids.

        Args:
            value (float): The pressure loss in Pascals (Pa).

        Returns:
            float: The pressure loss in Pascals (Pa).

        """
        return self.in_fluid.pressure - self.out_fluid.pressure

    @pressure_loss.setter
    def pressure_loss(self, value):
        out_pressure = self.in_fluid.pressure - value
        self.out_fluid.pressure = out_pressure
        logging.debug(f"setting pressure loss {value} Pa, new out pressure = {out_pressure}")

    @property
    def out_temperature(self):
        """
        Get or set the output temperature in Kelvin (K).

        If the phase changes during the process, a warning is issued.

        Args:
            value (float): The output temperature in Kelvin (K).

        Returns:
            float: The output temperature in Kelvin (K).

        """
        return self.out_fluid.temperature

    @out_temperature.setter
    def out_temperature(self, value):
        self.out_fluid.temperature = value
        if self.phase_change:
            warnings.warn("the phase changes, this could lead to some problems")

    @property
    def phase_change(self) -> bool:
        """
        Check if a phase change occurs between input and output fluids.

        Returns:
            bool: True if a phase change occurs, False otherwise.

        """
        return self.in_fluid.fluid.phase != self.out_fluid.fluid.phase

    @property
    def mass_flow(self):
        """
        Calculate and return the mass flow rate based on the volume flow rate and the mean fluid's density.

        Args:
            value (float): The mass flow rate in kg/s.

        Returns:
            float: The mass flow rate in kg/s.

        """
        value = self.volume_flow * self.mean_fluid.density
        return value

    @mass_flow.setter
    def mass_flow(self, value):
        self._volume_flow = value / self.mean_fluid.density

    def mass_flow_str(self):
        """
        Return a formatted string for the mass flow rate.

        Returns:
            str: A string containing the mass flow rate in kg/s.

        """
        return f"mass flow = %.5f kg/s" % self.mass_flow

    @property
    def heat_capacity_flow(self):
        return self.mass_flow * self.mean_fluid.specific_heat

    def heat_capacity_flow_str(self):
        """
        Return a formatted string for the heat capacity flow rate.

        Returns:
            str: A string containing the heat capacity flow rate in W/K.

        """
        return f"heat capacity flow: W_dot = %.5f W/K" % (self.heat_capacity_flow)

    @property
    def heat_flow(self):
        if self.phase_change:
            warnings.warn("the phase changes, this could lead to some problems")
        heat_flow_enthalpy = self.mass_flow * (self.in_fluid.fluid.enthalpy - self.out_fluid.fluid.enthalpy)
        # heat_flow_temps = self.heat_capacity_flow * (self.in_fluid.temperature - self.out_fluid.temperature)
        return heat_flow_enthalpy

    def heat_flow_str(self):
        """
        Return a formatted string for the heat flow rate.

        Returns:
            str: A string containing the heat flow rate in kW.

        """
        return f"heat flow: Q_dot = %.5f kW\n" % (self.heat_flow * 1e-3)

    def clone(self):
        """
        Create a new Flow object with the same properties.

        Returns:
            Flow: A new Flow object with identical properties.

        """
        new_flow = Flow(flow=self)
        return new_flow

    def clone_by_fluid(self, clone_fluid='in'):
        """
        Create a new Flow object by cloning and using the specified input or output fluid.

        Args:
            clone_fluid (str): Specifies whether to clone the 'in' or 'out' fluid.

        Returns:
            Flow: A new Flow object with the specified input or output fluid.

        Raises:
            NotImplementedError: If an unsupported value for clone_fluid is provided.

        """
        new_flow = self.clone()
        if clone_fluid == 'in':
            fluid = self.in_fluid
        elif clone_fluid == 'out':
            fluid = self.out_fluid
        else:
            raise NotImplementedError
        new_flow.in_fluid = fluid
        new_flow.out_fluid = fluid

        return new_flow

    def __repr__(self):
        output = f"Flow: id = {id(self)}\n"
        output += f"\t" + self.mass_flow_str() + "\n"
        output += f"\t" + self.heat_capacity_flow_str() + "\n"
        output += f"\t" + self.heat_flow_str() + "\n"
        output += f"Input Fluid:\n\t{self.in_fluid}\n"
        output += f"Output Fluid:\n\t{self.out_fluid}\n"
        return output
