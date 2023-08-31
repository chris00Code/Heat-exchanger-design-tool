import warnings

from numpy import exp

from .stream import Fluid, Flow
from .parts import Part


class HeatExchanger:
    def __init__(self, flow_1=None, flow_2=None, part: Part = None):
        self.flow_1 = flow_1
        self.flow_2 = flow_2
        self.part = part

    @property
    def flow_1(self):
        return self._flow_1

    @flow_1.setter
    def flow_1(self, value):
        if isinstance(value, Flow):
            self._flow_1 = value
        else:
            raise NotImplementedError

    @property
    def flow_2(self):
        return self._flow_2

    @flow_2.setter
    def flow_2(self, value):
        if isinstance(value, Flow):
            self._flow_2 = value
        else:
            raise NotImplementedError

    @property
    def part(self):
        return self._part

    @part.setter
    def part(self, value):
        if value is None:
            value = Part()
        self._part = value

    @property
    def heat_transfer_area(self):
        return self.part.heat_transfer_area

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        self.part.heat_transfer_area = value

    @property
    def heat_transfer_coefficient(self):
        return self.part.heat_transfer_coefficient

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        self.part.heat_transfer_coefficient = value

    @property
    def heat_transferability(self):
        return self.part.heat_transferability

    @heat_transferability.setter
    def heat_transferability(self, value):
        self.part.heat_transferability = value

    @property
    def heat_capacity_flow(self):
        return self.flow_1.heat_capacity_flow, self.flow_2.heat_capacity_flow

    @property
    def heat_flows(self):
        return self.flow_1.heat_flow, self.flow_2.heat_flow

    @property
    def pressure_loss(self):
        """
        calcs the pressure loss of the two fluids in the heat exchanger. flow 1 is assumened as the flow inside of the part.
        :return: pressure loss
        """
        zeta = self.part.pressure_coefficient
        hydraulic_diameter = self.part.hydraulic_diameter
        if isinstance(zeta, tuple):
            v_dot_1 = self.flow_1.volume_flow
            a_1 = self.part.flow_area
        else:
            value = NotImplemented
        return value

    @staticmethod
    def _calc_pressure_loss(zeta, velocity, density):
        return zeta * density / 2 * velocity ** 2

    def _calc_output(self):
        for i in range(5):
            temp_1_in = self.flow_1.in_fluid.temperature
            temp_2_in = self.flow_2.in_fluid.temperature
            p1, p2 = self.p
            temp_1_out = -p1 * (temp_1_in - temp_2_in) + temp_1_in
            temp_2_out = p2 * (temp_1_in - temp_2_in) + temp_2_in
            self.flow_1.out_temperature = temp_1_out
            self.flow_2.out_temperature = temp_2_out

    @property
    def ntu(self):
        kA = self.heat_transferability
        heat_capacity_flow_1 = self.flow_1.heat_capacity_flow
        heat_capacity_flow_2 = self.flow_2.heat_capacity_flow
        ntu1, ntu2 = NotImplemented, NotImplemented
        if kA is not NotImplemented and (heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            ntu1 = kA / heat_capacity_flow_1
            ntu2 = kA / heat_capacity_flow_2
        return ntu1, ntu2

    def ntu_str(self):
        output = "number of transfer units:\n"
        try:
            output += f"\tNTU_1 = %.3f\n\tNTU_2 = %.3f\n" % (self.ntu)
        except TypeError:
            output += "\tNot implemented\n"
        return output

    @property
    def r(self):
        heat_capacity_flow_1 = self.flow_1.heat_capacity_flow
        heat_capacity_flow_2 = self.flow_2.heat_capacity_flow
        if (heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            r1 = heat_capacity_flow_1 / heat_capacity_flow_2
            r2 = heat_capacity_flow_2 / heat_capacity_flow_1
        else:
            raise ValueError("heat capacity flow not defined")
        return r1, r2

    def r_str(self):
        output = "heat capacity flow ratios:\n"
        try:
            output += f"\tR_1 = %.3f\n\tR_2 = %.3f\n" % (self.r)
        except TypeError:
            output += "\tNot implemented\n"
        return output

    @property
    def p(self):
        pass
        raise NotImplementedError

    def p_str(self):
        output = "dimensionless temperature change:\n"
        try:
            output += f"\tP_1 = %.3f\n\tP_2 = %.3f\n" % (self.p)
        except TypeError:
            output += "\tNot implemented\n"
        except NotImplementedError:
            output += "\tnot defined for HeatExchanger"
        return output

    def dimensionless_parameters_str(self):
        return f"dimensionless parameters:\n" + self.ntu_str() + self.r_str() + self.p_str()

    def __repr__(self) -> str:
        output = f"\nheat exchanger:\n" \
                 f"\tid = {id(self)}\n" \
                 f"\ttype: {self.__class__.__name__}\n"
        output += "Flows:\n" \
                  f"Flow 1:\n{self.flow_1}\n" \
                  f"Flow 2:\n{self.flow_2}\n"
        output += "Parameters:\n"
        output += "\n" + self.dimensionless_parameters_str()
        return output


class ParallelFlow(HeatExchanger):
    @property
    def p(self):
        n1, n2 = self.ntu
        r1, r2 = self.r
        p1 = (1 - exp(-n1 * (1 + r1))) / (1 + r1)
        p2 = (1 - exp(-n2 * (1 + r2))) / (1 + r2)
        return p1, p2


class CounterCurrentFlow(HeatExchanger):
    @property
    def p(self):
        n1, n2 = self.ntu
        r1, r2 = self.r
        if r1 == 1:
            p1 = n1 / (1 + n1)
        else:
            p1 = (1 - exp(n1 * (r1 - 1))) / (1 - r1 * exp(n1 * (r1 - 1)))
        if r2 == 1:
            p2 = n2 / (1 + n2)
        else:
            p2 = (1 - exp(n2 * (r2 - 1))) / (1 - r2 * exp(n2 * (r2 - 1)))
        return p1, p2


class CrossFlowOneRow(HeatExchanger):
    @property
    def p(self):
        n1, n2 = self.ntu
        r1, r2 = self.r
        p1 = 1 - exp((exp(-r1 * n1) - 1) / r1)
        # p2 = 1 - exp((exp(-r2 * n2) - 1) / r2)
        p2 = r1 * p1
        return p1, p2
