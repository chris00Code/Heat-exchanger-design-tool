from math import pi, log
import warnings
from .utils import get_def_or_calc_value


class Part:
    """
    A base class representing a heat exchanger part.

    Attributes:
        heat_transfer_area (float): The heat transfer area of the part in square meters (m^2).
        heat_transfer_coefficient (float): The heat transfer coefficient of the part in W/(m^2 K).
        heat_transferability (float): The heat transferability of the part in W/K.

    """

    def __init__(self, heat_transferability: float = NotImplemented, heat_transfer_area: float = NotImplemented,
                 heat_transfer_coefficient: float = NotImplemented):

        self.heat_transfer_area = heat_transfer_area
        self.heat_transfer_coefficient = heat_transfer_coefficient
        self.heat_transferability = heat_transferability

    # heat parameters

    @property
    def heat_transfer_area(self):
        """
        Get or set the heat transfer area of the part in square meters (m^2).

        Args:
            value (float): The new heat transfer area to set in square meters (m^2).

        Raises:
            ValueError: If the provided heat transfer area value is not valid.

        Returns:
            float: The heat transfer area of the part in square meters (m^2).
        """
        if not self._is_heat_parameter_consistent():
            warnings.warn(
                "heat transfer parameters are not consistent, defined parameter will be returned (not calculated one)")
        return self._heat_transfer_area

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        if not self._is_heat_parameter_consistent(transfer_area=value):
            warnings.warn("heat transfer parameters not consistent")
        self._heat_transfer_area = value

    def heat_transfer_area_str(self) -> str:
        """
        Returns a string representation of the heat transfer area.

        Returns:
            str: The heat transfer area string representation.
        """
        try:
            return f"\theat transfer area: %.4f m^2\n" % self.heat_transfer_area
        except TypeError:
            return ""

    @property
    def heat_transfer_coefficient(self):
        """
        Get or set the heat transfer coefficient of the part in W/(m^2 K).

        Args:
            value (float): The new heat transfer coefficient to set in W/(m^2 K).

        Raises:
            ValueError: If the provided heat transfer coefficient value is not valid.

        Returns:
            float: The heat transfer coefficient of the part in W/(m^2 K).
        """

        if not self._is_heat_parameter_consistent():
            warnings.warn(
                "heat transfer parameters are not consistent, defined parameter will be returned (not calculated one)")
        return self._heat_transfer_coefficient

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        if not self._is_heat_parameter_consistent(transfer_coefficient=value):
            warnings.warn("heat transfer parameters not consistent")
        self._heat_transfer_coefficient = value

    def heat_transfer_coefficient_str(self) -> str:
        """
        Returns a string representation of the heat transfer coefficient.

        Returns:
            str: The heat transfer coefficient string representation.
        """

        try:
            return f"\theat transfer coefficient: %.2f W/(m^2 K)\n" % (self.heat_transfer_coefficient)
        except TypeError:
            return ""

    @property
    def heat_transferability(self):
        """
        Get or set the heat transferability of the part in W/K.

        Args:
            value (float): The new heat transferability to set in W/K.

        Raises:
            ValueError: If the provided heat transferability value is not valid.

        Returns:
            float: The heat transferability of the part in W/K.
        """

        if not self._is_heat_parameter_consistent():
            warnings.warn(
                "heat transfer parameters are not consistent, defined parameter will be returned (not calculated one)")
        value = self._heat_transferability
        if value is NotImplemented:
            try:
                value = self.heat_transfer_area * self.heat_transfer_coefficient
            except TypeError:
                pass
        return value

    @heat_transferability.setter
    def heat_transferability(self, value):
        if not self._is_heat_parameter_consistent(transferability=value):
            warnings.warn("heat transfer parameters not consistent")
        self._heat_transferability = value

    def heat_transferability_str(self):
        """
        Returns a string representation of the heat transferability.

        Returns:
            str: The heat transferability string representation.
        """

        try:
            output = f"\theat transferability: {self.heat_transferability:.3f} W/K\n"
        except TypeError:
            output = ""
        return output

    def _is_heat_parameter_consistent(self, transferability=None, transfer_coefficient=None, transfer_area=None):
        """
        Check if heat transfer parameters are consistent.

        Args:
            transferability (float): The heat transferability value to check.
            transfer_coefficient (float): The heat transfer coefficient value to check.
            transfer_area (float): The heat transfer area value to check.

        Returns:
            bool: True if the heat transfer parameters are consistent, False otherwise.
        """

        if transferability is None:
            try:
                transferability = self._heat_transferability
            except AttributeError:
                return True
        if transfer_coefficient is None:
            try:
                transfer_coefficient = self._heat_transfer_coefficient
            except AttributeError:
                return True
        if transfer_area is None:
            try:
                transfer_area = self._heat_transfer_area
            except AttributeError:
                return True
        if any(item is NotImplemented for item in [transferability, transfer_coefficient, transfer_area]):
            return True
        else:
            return transferability == transfer_coefficient * transfer_area

    # geometric parameters

    @property
    def area(self):
        """
        Get or set the area of the part.

        Args:
            value (float): The new area to set.

        Returns:
            float: The area of the part.
        """

        try:
            value = self._area
        except AttributeError:
            value = None
        finally:
            return value

    @area.setter
    def area(self, value):
        self._area = value

    def geometrics_str(self):
        """
        Returns a string representation of geometric properties.

        Returns:
            str: The geometric properties string representation.
        """
        return ""

    # hydraulic parameters

    @property
    def flow_area(self):
        """
        Get or set the flow area (to calc flow rates) of the part in square meters (m^2).

        Args:
            value (float): The new flow area to set in square meters (m^2).

        Returns:
            float: The flow area of the part in square meters (m^2).
        """

        try:
            value = self._flow_area
        except AttributeError:
            value = None
        finally:
            return value

    @flow_area.setter
    def flow_area(self, value):
        self._flow_area = value

    def flow_area_str(self) -> str:
        try:
            return f"\tflow area = %.6f m^2\n" % (self.flow_area * 1)
        except TypeError:
            return ""

    @property
    def hydraulic_diameter(self):
        """
        Get or set the hydraulic diameter of the part in meters (m).

        Args:
            value (float): The new hydraulic diameter to set in meters (m).

        Returns:
            float: The hydraulic diameter of the part in meters (m).
        """

        try:
            value = self._hydraulic_diameter
        except AttributeError:
            value = None
        finally:
            return value

    @hydraulic_diameter.setter
    def hydraulic_diameter(self, value):
        self._hydraulic_diameter = value

    def hydraulic_diameter_str(self) -> str:
        """
        Returns a string representation of the hydraulic diameter.

        Returns:
            str: The hydraulic diameter string representation.
        """

        try:
            return f"\thydraulic diameter = %.4f m\n" % (self.hydraulic_diameter * 1)
        except TypeError:
            return ""

    @property
    def pressure_coefficient(self):
        """
        Get or set the pressure coefficient of the part.

        Args:
            value (float): The new pressure coefficient to set.

        Returns:
            float: The pressure coefficient of the part.
        """

        try:
            value = self._pressure_coefficient
        except AttributeError:
            value = None
        return value

    @pressure_coefficient.setter
    def pressure_coefficient(self, value):
        self._pressure_coefficient = value

    def pressure_coefficient_str(self) -> str:
        """
        Returns a string representation of the pressure coefficient.

        Returns:
            str: The pressure coefficient string representation.
        """

        try:
            return f"\tpressure coefficient = %.4f\n" % (self.pressure_coefficient)
        except TypeError:
            return ""

    def hydraulic_properties_str(self):
        """
        Returns a string representation of hydraulic properties.

        Returns:
            str: The hydraulic properties string representation.
        """

        output = f"\nhydraulic properties:\n" + \
                 self.flow_area_str() + \
                 self.hydraulic_diameter_str() + \
                 self.pressure_coefficient_str()
        return output

    def thermic_properties_str(self):
        """
        Returns a string representation of thermic properties.

        Returns:
            str: The thermic properties string representation.
        """

        output = f"\nthermic properties:\n" + \
                 self.heat_transferability_str() + \
                 self.heat_transfer_area_str() + \
                 self.heat_transfer_coefficient_str()
        return output

    def __repr__(self):
        output = f"part:\n" \
                 f"\t id = {id(self)}\n" \
                 f"\t typ: {self.__class__.__name__}\n"
        output += f"\ngeometric properties:\n" + \
                  self.geometrics_str()
        output += self.hydraulic_properties_str()
        output += self.thermic_properties_str()
        return output


class Pipe(Part):
    """
    A class representing a pipe.

    Attributes:
        diameter_in (float): The inner diameter of the pipe in meters (m).
        diameter_out (float): The outer diameter of the pipe in meters (m).
        length (float): The length of the pipe in meters (m).

    """

    def __init__(self, diameter_in: float = None, diameter_out: float = None, length: float = NotImplemented, **kwargs):
        self.diameter_in = diameter_in
        self.diameter_out = diameter_out
        self.length = length
        super().__init__(**kwargs)

    @property
    def length(self):
        """
        Get or set the length of the pipe in meters (m).

        Args:
            value (float): The new length to set in meters (m).

        Returns:
            float: The length of the pipe in meters (m).
        """
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def heat_transfer_area(self):
        try:
            d_in, d_out = self.diameter_in, self.diameter_out
            l = self.length
            value = (d_in - d_out) / log(d_in / d_out) * pi * l
        except TypeError:
            value = NotImplemented
        if not self._is_heat_parameter_consistent(transfer_area=value):
            warnings.warn("heat transfer parameters not consistent")
        self._heat_transfer_area = value

        return super().heat_transfer_area

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        if value is not NotImplemented:
            warnings.warn("function not available, value is not set")
        pass

    @property
    def area(self):
        return self.diameter_out ** 2 * pi / 4

    @property
    def flow_area(self):
        return self.diameter_in ** 2 * pi / 4

    @property
    def hydraulic_diameter(self):
        return self.diameter_in

    @property
    def pipe_resistance_coefficient(self):
        try:
            return self._pipe_resistance_number
        except AttributeError:
            return None

    @pipe_resistance_coefficient.setter
    def pipe_resistance_coefficient(self, value):
        self._pipe_resistance_number = value

    @property
    def pressure_coefficient(self):
        try:
            value = self.pipe_resistance_coefficient * self.length / self.hydraulic_diameter
        except TypeError:
            value = None
        return value

    def geometrics_str(self):
        output = ""
        try:
            output += f"\tlength = {self.length:.5f} m\n"
        except TypeError:
            pass
        try:
            output += f"\tdiameter: in = {self.diameter_in * 1:.5f} m, out = {self.diameter_out * 1:.5f} m\n"
        except TypeError:
            pass
        return output


class StraightPipe(Pipe):
    """
    A class representing a straight pipe.

    This class inherits from Pipe and does not have any additional attributes or methods.

    """
    pass


class PipeLayout(Part):
    """
    A class representing a pipe bundle in a heat exchanger.

    Attributes:
        pipe (Pipe): The type of pipe used in the layout.
        number_pipes (float): The number of pipes in the layout.
        pattern (str): The pattern of pipe arrangement (e.g., 'square', 'triangular').
        pipe_pitch (float): The pitch between pipes in meters (m).

    """

    def __init__(self, pipe: Pipe, number_pipes: float = 1, pattern: str = 'square', pipe_pitch: float = None):
        self.pipe = pipe
        self.number_pipes = number_pipes
        self.pattern = pattern
        self.pipe_pitch = pipe_pitch

        super().__init__()

    @property
    def heat_transfer_area(self):
        """
        Get or set the heat transfer area of the pipe bundle in square meters (m^2).

        This property calculates the heat transfer area by the product of the heat transfer area of a single pipe and the number of those.

        Returns:
            float: The heat transfer area of the pipe bundle in square meters (m^2).
        """
        def_value = super().heat_transfer_area
        calc_value = self.number_pipes * self.pipe.heat_transfer_area
        return get_def_or_calc_value(def_value, calc_value)

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        Part.heat_transfer_area.fset(self, value)

    @property
    def heat_transfer_coefficient(self):
        def_value = super().heat_transfer_coefficient
        calc_value = self.pipe.heat_transfer_coefficient
        return get_def_or_calc_value(def_value, calc_value)

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        Part.heat_transfer_coefficient.fset(self, value)

    @property
    def heat_transferability(self):
        return super().heat_transferability

    @heat_transferability.setter
    def heat_transferability(self, value):
        Part.heat_transferability.fset(self, value)

    def geometrics_str(self):
        output = ""
        output += f"\tpipe type: {self.pipe.__class__.__name__}\n"
        try:
            output += self.pipe.geometrics_str()
        except TypeError:
            pass
        try:
            output += f"\tnumber of pipes: {self.number_pipes}\n"
        except TypeError:
            pass
        try:
            output += f"\tpipe pattern: {self.pattern}\n"
        except TypeError:
            pass
        return output

    @property
    def number_pipes(self):
        """
        Set the number of pipes in the layout.

        Args:
            value (float): The new number of pipes to set.
        """
        return self._number_pipes

    @number_pipes.setter
    def number_pipes(self, value):
        self._number_pipes = value

    @property
    def flow_area(self):
        return self.number_pipes * self.pipe.flow_area

    @property
    def pressure_coefficient_shellside(self):
        """
        Get or set the pressure coefficient on the shell side.

        Returns:
            float: The pressure coefficient on the shell side.
        """
        return self._pressure_coefficient_shellside

    @pressure_coefficient_shellside.setter
    def pressure_coefficient_shellside(self, value):
        self._pressure_coefficient_shellside = value

    @property
    def pressure_coefficient_tubeside(self):
        """
        Get or set the pressure coefficient on the tube side.

        Returns:
            float: The pressure coefficient on the tube side.
        """
        try:
            return self._pressure_coefficient_tubeside
        except AttributeError:
            # @TODO calculate number of tubes
            return self.pipe.pressure_coefficient

    @pressure_coefficient_tubeside.setter
    def pressure_coefficient_tubeside(self, value):
        self._pressure_coefficient_tubeside = value


class ShellGeometry:
    """
    A base class representing the geometry of the shell side of a heat exchanger.

    Attributes:
        length (float): The length of the shell in meters (m).

    """

    def __init__(self, length: float = None):
        self.length = length

    @property
    def area_in(self):
        """
        Get the cross-sectional area on the shell side.

        Returns:
            float: The cross-sectional area in square meters (m^2).

        """
        pass

    def geometrics_str(self):
        """
        Get a string representation of the geometric properties.

        Returns:
            str: A string containing geometric properties information.

        """

        output = ""
        try:
            output += f"\tlength: {self.length:>7.3f} m\n"
        except TypeError:
            pass
        output += self.geometrics_additional_str()
        return output

    def __repr__(self):
        output = f"shell geometry: {self.__class__.__name__}\n"
        output += self.geometrics_str()
        return output

    def geometrics_additional_str(self):
        """
        Get additional geometric properties as a string.

        Returns:
            str: A string containing additional geometric properties information.

        """
        return ""


class SquareShellGeometry(ShellGeometry):
    """
    A class representing square shell geometry in a heat exchanger.

    Attributes:
        width_in (float): The inner width of the square shell in meters (m).
        height_in (float): The inner height of the square shell in meters (m).

    """

    def __init__(self, length: float = 1, width_in: float = 1, height_in: float = 1):
        super().__init__(length)
        self.width_in = width_in
        self.height_in = height_in

    @property
    def area_in(self):
        return self.height_in * self.width_in

    def geometrics_additional_str(self):
        output = f"\theight: {self.height_in:>7.3f} m\n" \
                 f"\twidth: {self.width_in:>7.3f} m\n"
        return output


class TubeShellGeometry(ShellGeometry):
    """
    A class representing tube shell geometry in a heat exchanger.

    Attributes:
        diameter_in (float): The inner diameter of the shell in meters (m).

    """

    def __init__(self, length: float = 1, diameter_in: float = 1):
        super().__init__(length)
        self.diameter_in = diameter_in

    @property
    def area_in(self):
        return self.diameter_in ** 2 * pi / 4

    def geometrics_additional_str(self):
        output = f"\tdiameter in = {self.diameter_in:.3f} m\n"
        return output


class Baffle:
    """
    A base class representing (vertical) baffles in a heat exchanger.

    Attributes:
        number_baffles (int): The number of baffles in the heat exchanger.

    """

    @property
    def number_baffles(self):
        """
        Get or set the number of baffles in the heat exchanger.

        Args:
            value (int): The new number of baffles to set.

        Returns:
            int: The number of baffles in the heat exchanger.

        """
        return self._number_baffles

    @number_baffles.setter
    def number_baffles(self, value):
        self._number_baffles = value

    def ad_str(self):
        """
        Get additional information about baffles as a string.

        Returns:
            str: Additional information about baffles.

        """
        pass

    def __repr__(self):
        output = f"baffle: type = {self.__class__.__name__}\n"
        output += f"\tnumber of baffles = {self.number_baffles}\n"
        output += self.ad_str()
        return output


class SegmentalBaffle(Baffle):
    """
    A class representing segmental baffles in a heat exchanger.

    Attributes:
        number_baffles (int): The number of segmental baffles in the heat exchanger.
        baffle_cut (int): The percentage of baffle cut.

    """

    def __init__(self, number, baffle_cut=50):
        self.number_baffles = number
        self.baffle_cut = baffle_cut

    @property
    def baffle_cut(self):
        """
        Get or set the percentage of baffle cut.

        Args:
            value (int): The new percentage of baffle cut to set.

        Returns:
            int: The percentage of baffle cut.

        """
        return self._baffle_cut

    @baffle_cut.setter
    def baffle_cut(self, value):
        self._baffle_cut = value

    def ad_str(self):
        """
        Get additional information about segmental baffles as a string.

        Returns:
            str: Additional information about segmental baffles.

        """
        output = f"\tbaffle cut: {self.baffle_cut} %"
        return output


class Inlets:
    """
    A class representing inlets positions for the flow in a heat exchanger and defining the flow throw it.

    The definition is done using two strings: `flow_order_1` and `flow_order_2`. These strings follow a specific convention to determine how
    the respective fluid streams move through the network. Here is a detailed explanation of the convention:

    The first character in the string describes the vertical position of the inlet:
        - 'u' stands for upper (top).
        - 'd' stands for down (bottom).

    The second character in the string describes the horizontal position of the inlet:
        - 'r' stands for right.
        - 'l' stands for left.

    The flow direction through the heat exchanger is additionally described by:
    - Following that is a '2' indicating a change in direction.

    After that, the direction in which the fluid flows is specified:
        - 'd' stands for downward flow.
        - 'u' stands for upward flow.
        - 'l' stands for flow to the left.
        - 'r' stands for flow to the right.

    Attributes:
        flow_order_1 (str): The flow order for the first inlet (e.g., 'ul', 'ur', 'dl', 'dr').
        flow_order_2 (str): The flow order for the second inlet (e.g., 'ul', 'ur', 'dl', 'dr').

    """
    positions = {
        'ul': 'upp left',
        'ur': 'upp right',
        'dl': 'down left',
        'dr': 'down right'
    }

    def __init__(self, shell_inlet: str = None, tube_inlet: str = None):
        self.flow_order_1 = shell_inlet
        self.flow_order_2 = tube_inlet

    @property
    def flow_order_1(self):
        """
        Get or set the flow order for the first inlet.

        Args:
            value (str): The new flow order for the first inlet.

        Returns:
            str: The flow order for the first inlet.

        """
        return self._flow_order_1

    @flow_order_1.setter
    def flow_order_1(self, value):
        if value in self.positions:
            match value[0]:
                case 'u':
                    value += '2d'
                case 'd':
                    value += '2u'
                case None:
                    pass
                case _:
                    raise ValueError
        else:
            value = None
        self._flow_order_1 = value

    @property
    def flow_order_2(self):
        """
         Set the flow order for the first inlet.

         Args:
             value (str): The new flow order for the first inlet.

         Raises:
             ValueError: If the provided value is not valid according to the convention.

         """
        return self._flow_order_2

    @flow_order_2.setter
    def flow_order_2(self, value):
        if value in self.positions:
            match value[1]:
                case 'l':
                    value += '2r'
                case 'r':
                    value += '2l'
                case None:
                    pass
                case _:
                    raise ValueError
        else:
            value = None
        self._flow_order_2 = value

    def __repr__(self):
        value = [self.flow_order_1, self.flow_order_2]
        output = f"flow orders:\n"
        if all(value) is None:
            return f""
        if value[0] is not None:
            output += f"\tshell flow (flow 1): {value[0]}\n"
        if value[1] is not None:
            output += f"\ttube flow (flow 2): {value[1]}\n"
        return output


class Assembly(Part):
    """
    A class representing the assembly of heat exchanger components.

    Attributes:
        shell (ShellGeometry): The shell geometry of the heat exchanger.
        tube_passes (int): The number of tube passes in the heat exchanger.
        pipe_layout (PipeLayout): The layout of pipes in the heat exchanger.
        baffles (Baffle): The baffles used in the heat exchanger.
        flow_orders (Inlets): The flow orders for shell and tube inlets.

    """

    def __init__(self, shell: ShellGeometry, pipe_layout: PipeLayout, tube_passes: int = 1,
                 baffle: Baffle = NotImplemented,
                 inlets: Inlets = Inlets()):
        self.shell = shell
        self.tube_passes = tube_passes
        self.pipe_layout = pipe_layout

        self.baffles = baffle
        self.flow_orders = inlets

        super().__init__()

    @property
    def heat_transfer_area(self):
        def_value = super().heat_transfer_area
        calc_value = self.pipe_layout.heat_transfer_area
        return get_def_or_calc_value(def_value, calc_value)

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        Part.heat_transfer_area.fset(self, value)

    @property
    def heat_transfer_coefficient(self):
        def_value = super().heat_transfer_coefficient
        calc_value = self.pipe_layout.heat_transfer_coefficient
        return get_def_or_calc_value(def_value, calc_value)

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        Part.heat_transfer_coefficient.fset(self, value)

    @property
    def heat_transferability(self):
        return super().heat_transferability

    @heat_transferability.setter
    def heat_transferability(self, value):
        Part.heat_transferability.fset(self, value)

    @property
    def pipe_layout(self):
        """
        Get or set the layout of pipes in the assembly.

        Returns:
            PipeLayout: The layout of pipes.

        """
        return self._pipe_layout

    @pipe_layout.setter
    def pipe_layout(self, value):
        if isinstance(value, PipeLayout):
            if value.pipe.length is NotImplemented:
                # assumes tubesheets not bends
                value.pipe.length = self.shell.length * self.tube_passes
            self._pipe_layout = value
        else:
            raise NotImplementedError

    @property
    def flow_orders(self):
        """
        Get the flow orders for shell and tube inlets.

        Returns:
            tuple: A tuple containing the flow orders for shell and tube inlets.

        """
        orders = self._flow_orders
        return orders.flow_order_1, orders.flow_order_2

    @flow_orders.setter
    def flow_orders(self, value):
        if isinstance(value, Inlets):
            self._flow_orders = value
        else:
            raise NotImplementedError

    def flow_orders_str(self):
        """
        Get a string representation of the flow orders for shell and tube inlets.

        Returns:
            str: A string describing the flow orders.

        """
        return str(self._flow_orders)

    @property
    def flow_area(self):
        """
        Get the flow area for shell and tube sides.

        They ara calculated by the Cross-sectional area usable by the fluid.

        Returns:
            tuple: A tuple containing the flow area coefficients for shell and tube sides.

        """
        area_shell_inside = self.pipe_layout.flow_area
        area_shell_outside = self.shell.area_in - self.pipe_layout.pipe.area
        return area_shell_inside, area_shell_outside

    def flow_area_str(self):
        """
        Get a string representation of the flow area coefficients for shell and tube sides.

        Returns:
            str: A string describing the flow area coefficients.

        """
        value = self.flow_area
        output = f"\tflow area coefficient:\n"
        if all(value) is None:
            return f""
        if value[0] is not None:
            output += f"\t\tshell side: {value[0]:.6f} m^2\n"
        if value[1] is not None:
            output += f"\t\ttube side: {value[1]:.6f} m^2\n"
        return output

    @property
    def pressure_coefficient(self):
        try:
            shell = self.pressure_coefficient_shellside
        except AttributeError:
            shell = None
        try:
            tube = self.pressure_coefficient_tubeside
        except AttributeError:
            tube = None
        return shell, tube

    @property
    def pressure_coefficient_shellside(self):
        """
        Get or set the pressure coefficient for the shell side.

        Returns:
            float: The pressure coefficient for the shell side.

        """
        try:
            return self._pressure_coefficient_shellside
        except AttributeError:
            return self.pipe_layout.pressure_coefficient_shellside

    @pressure_coefficient_shellside.setter
    def pressure_coefficient_shellside(self, value):
        self._pressure_coefficient_shellside = value

    @property
    def pressure_coefficient_tubeside(self):
        """
        Get or set the pressure coefficient for the tube side.

        Returns:
            float: The pressure coefficient for the tube side.

        """
        try:
            return self._pressure_coefficient_tubeside
        except AttributeError:
            return self.pipe_layout.pressure_coefficient_tubeside

    @pressure_coefficient_tubeside.setter
    def pressure_coefficient_tubeside(self, value):
        self._pressure_coefficient_tubeside = value

    def pressure_coefficient_str(self) -> str:
        """
        Get a string representation of the pressure coefficients for shell and tube sides.

        Returns:
            str: A string describing the pressure coefficients.

        """
        value = self.pressure_coefficient
        output = f"\tpressure coefficient:\n"
        if all(value) is None:
            return f""
        if value[0] is not None:
            output += f"\t\tshell side: zeta = {value[0]:.3f}\n"
        if value[1] is not None:
            output += f"\t\ttube side: zeta = {value[1]:.3f}\n"
        return output

    def __repr__(self):
        output = "Heat exchanger components:\n"
        output += str(self.shell)
        output += f"PipeLayout:\n" + self.pipe_layout.geometrics_str()
        output += self.hydraulic_properties_str()
        output += self.thermic_properties_str()
        output += f"\nTube passes: number={self.tube_passes}\n"
        output += f"\nBaffles:\n" + str(self.baffles) + "\n\n"
        output += self.flow_orders_str()
        return output
