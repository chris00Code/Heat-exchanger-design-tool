from math import pi, log


class Part:
    def __init__(self, heat_transferability: float = None, heat_transfer_area: float = None,
                 heat_transfer_coefficient: float = None):

        if heat_transferability is None:
            if heat_transfer_area is None and heat_transfer_coefficient is None:
                self.heat_transferability = 0.0
            else:
                self.heat_transfer_area = heat_transfer_area
                self.heat_transfer_coefficient = heat_transfer_coefficient
        else:
            self.heat_transferability = heat_transferability
        # @TODO implement more init parameters

    @property
    def heat_transfer_area(self):
        try:
            value = self._heat_transfer_area
        except AttributeError:
            value = None
        finally:
            return value

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        if self.heat_transferability is None:
            self._heat_transfer_area = value
        else:
            raise AttributeError("heat_transferability already set")

    def heat_transfer_area_str(self) -> str:
        try:
            return f"\theat transfer area: %.4f m^2\n" % self.heat_transfer_area
        except TypeError:
            return ""

    @property
    def heat_transfer_coefficient(self):
        try:
            value = self._heat_transfer_coefficient
        except AttributeError:
            value = None
        finally:
            return value

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        if self.heat_transferability is None:
            self._heat_transfer_coefficient = value
        else:
            raise AttributeError("heat_transferability already set")

    def heat_transfer_coefficient_str(self) -> str:
        try:
            return f"\theat transfer coefficient: %.2f W/(m^2 K)\n" % (self.heat_transfer_coefficient)
        except TypeError:
            return ""

    @property
    def heat_transferability(self):
        try:
            value = self._heat_transferability
        except AttributeError:
            try:
                value = self.heat_transfer_area * self.heat_transfer_coefficient
            except TypeError:
                value = None
        return value

    @heat_transferability.setter
    def heat_transferability(self, value):
        # @TODO better handling requiered
        try:
            del self._heat_transfer_area
            del self._heat_transfer_coefficient
        except AttributeError:
            pass
        self._heat_transferability = value

    def heat_transferability_str(self):
        try:
            output = f"\theat transferability: {self.heat_transferability:.3f} W/K\n"
        except TypeError:
            output = ""
        return output

    @property
    def area(self):
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
        return ""

    @property
    def flow_area(self):
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
        try:
            return f"\thydraulic diameter = %.4f m\n" % (self.hydraulic_diameter * 1)
        except TypeError:
            return ""

    @property
    def pressure_coefficient(self):
        try:
            value = self._pressure_coefficient
        except AttributeError:
            value = None
        return value

    @pressure_coefficient.setter
    def pressure_coefficient(self, value):
        self._pressure_coefficient = value

    def pressure_coefficient_str(self) -> str:
        try:
            return f"\tpressure coefficient = %.4f\n" % (self.pressure_coefficient)
        except TypeError:
            return ""

    def hydraulic_properties_str(self):
        output = f"\nhydraulic properties:\n" + \
                 self.flow_area_str() + \
                 self.hydraulic_diameter_str() + \
                 self.pressure_coefficient_str()
        return output

    def thermic_properties_str(self):
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
    def __init__(self, diameter_in: float = None, diameter_out: float = None, length: float = None):
        self.diameter_in = diameter_in
        self.diameter_out = diameter_out
        self.length = length

    @property
    def length(self):
        try:
            value = self._length
        except AttributeError:
            value = None
        return value

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
            value = None
        return value

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
    pass


class PipeLayout(Part):
    def __init__(self, pipe: Pipe, number_pipes: float = 1, pattern: str = 'square', pipe_pitch: float = None):
        self.pipe = pipe
        self.number_pipes = number_pipes
        self.pattern = pattern
        self.pipe_pitch = pipe_pitch

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
        return self._number_pipes

    @number_pipes.setter
    def number_pipes(self, value):
        self._number_pipes = value

    @property
    def heat_transfer_area(self):
        value = self.number_pipes * self.pipe.heat_transfer_area
        return value

    @property
    def heat_transfer_coefficient(self):
        value = super().heat_transfer_coefficient
        if value is None:
            value = self.pipe.heat_transfer_coefficient
        return value

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        self._heat_transfer_coefficient = value

    @property
    def heat_transferability(self):
        return super().heat_transferability

    @property
    def flow_area(self):
        return self.number_pipes * self.pipe.flow_area

    @property
    def pressure_coefficient_shellside(self):
        return self._pressure_coefficient_shellside

    @pressure_coefficient_shellside.setter
    def pressure_coefficient_shellside(self, value):
        self._pressure_coefficient_shellside = value

    @property
    def pressure_coefficient_tubeside(self):
        try:
            return self._pressure_coefficient_tubeside
        except AttributeError:
            # @TODO calculate number of tubes
            return self.pipe.pressure_coefficient

    @pressure_coefficient_tubeside.setter
    def pressure_coefficient_tubeside(self, value):
        self._pressure_coefficient_tubeside = value


class ShellGeometry:
    def __init__(self, length: float = None):
        self.length = length

    @property
    def area_in(self):
        pass

    def geometrics_str(self):
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
        return ""


class SquareShellGeometry(ShellGeometry):
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
    @property
    def number_baffles(self):
        return self._number_baffles

    @number_baffles.setter
    def number_baffles(self, value):
        self._number_baffles = value

    def ad_str(self):
        pass

    def __repr__(self):
        output = f"baffle: type = {self.__class__.__name__}\n"
        output += f"\tnumber of baffles = {self.number_baffles}\n"
        output += self.ad_str()
        return output


class SegmentalBaffle(Baffle):
    def __init__(self, number, baffle_cut):
        self.number_baffles = number
        self.baffle_cut = baffle_cut

    @property
    def baffle_cut(self):
        return self._baffle_cut

    @baffle_cut.setter
    def baffle_cut(self, value):
        self._baffle_cut = value

    def ad_str(self):
        output = f"\tbaffle cut: {self.baffle_cut} %"
        return output


class Inlets:
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
    def __init__(self, shell: ShellGeometry, pipe_layout: PipeLayout, tube_passes: int = 1,
                 baffle: Baffle = NotImplemented,
                 inlets: Inlets = Inlets()):
        self.shell = shell
        self.pipe_layout = pipe_layout
        self.tube_passes = tube_passes
        self.baffles = baffle
        self.flow_orders = inlets

    @property
    def pipe_layout(self):
        return self._pipe_layout

    @pipe_layout.setter
    def pipe_layout(self, value):
        if isinstance(value, PipeLayout):
            if value.pipe.length is None:
                value.pipe.length = self.shell.length
            self._pipe_layout = value
        else:
            raise NotImplementedError

    @property
    def flow_orders(self):
        orders = self._flow_orders
        return orders.flow_order_1, orders.flow_order_2

    @flow_orders.setter
    def flow_orders(self, value):
        if isinstance(value, Inlets):
            self._flow_orders = value
        else:
            raise NotImplementedError

    def flow_orders_str(self):
        return str(self._flow_orders)

    @property
    def heat_transfer_area(self):
        return self.pipe_layout.heat_transfer_area

    @property
    def heat_transfer_coefficient(self):
        value = super().heat_transfer_coefficient
        if value is None:
            value = self.pipe_layout.heat_transfer_coefficient
        return value

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        self._heat_transfer_coefficient = value

    @property
    def flow_area(self):
        area_shell_inside = self.pipe_layout.flow_area
        area_shell_outside = self.shell.area_in - self.pipe_layout.pipe.area
        return area_shell_inside, area_shell_outside

    def flow_area_str(self):
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
        try:
            return self._pressure_coefficient_shellside
        except AttributeError:
            return self.pipe_layout.pressure_coefficient_shellside

    @pressure_coefficient_shellside.setter
    def pressure_coefficient_shellside(self, value):
        self._pressure_coefficient_shellside = value

    @property
    def pressure_coefficient_tubeside(self):
        try:
            return self._pressure_coefficient_tubeside
        except AttributeError:
            return self.pipe_layout.pressure_coefficient_tubeside

    @pressure_coefficient_tubeside.setter
    def pressure_coefficient_tubeside(self, value):
        self._pressure_coefficient_tubeside = value

    def pressure_coefficient_str(self) -> str:
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
