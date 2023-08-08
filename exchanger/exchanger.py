import stream
from stream import Fluid, Flow
from parts import Part
from numpy import exp


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
            NotImplementedError

    @property
    def flow_2(self):
        return self._flow_2

    @flow_2.setter
    def flow_2(self, value):
        if isinstance(value, Flow):
            self._flow_2 = value
        else:
            NotImplementedError

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
    def ntu(self):
        kA = self.heat_transferability
        heat_capacity_flow_1 = self.flow_1.heat_capacity_flow
        heat_capacity_flow_2 = self.flow_2.heat_capacity_flow
        if (kA and heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            ntu1 = kA / heat_capacity_flow_1
            ntu2 = kA / heat_capacity_flow_2
        return ntu1, ntu2

    def ntu_str(self):
        try:
            return f"number of transfer units:\nNTU_1 = %.3f\nNTU_2 = %.3f\n" % (self.ntu)
        except TypeError:
            raise NotImplementedError

    @property
    def r(self):
        heat_capacity_flow_1 = self.flow_1.heat_capacity_flow
        heat_capacity_flow_2 = self.flow_2.heat_capacity_flow
        if (heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            r1 = heat_capacity_flow_1 / heat_capacity_flow_2
            r2 = heat_capacity_flow_2 / heat_capacity_flow_1
        return r1, r2

    def r_str(self):
        try:
            return f"heat capacity flow ratios:\nR_1 = %.3f\nR_2 = %.3f\n" % (self.r)
        except TypeError:
            raise NotImplementedError

    @property
    def p(self):
        pass
        raise NotImplementedError

    def p_str(self):
        try:
            return f"dimensionless temperature change:\nP_1 = %.3f\nP_2 = %.3f\n" % (self.p)
        except TypeError:
            raise NotImplementedError
        except NotImplementedError:
            return f"dimensionless temperature change:\nnot defined for HeatExchanger"

    def dimensionless_parameters_str(self):
        return f"dimensionless parameters:\n" + self.ntu_str() + self.r_str() + self.p_str()

    def repr_short(self):
        output = f"Typ: {self.__class__.__name__},Id:{id(self)} \n\n"
        output += f"Wärmestrom:\n" \
                  f"Fld1: {self.heat_flows[0]}, Fld2: {self.heat_flows[1]}\n\n"
        output += f"Inputs: \n" \
                  f"Fluid 1:{self.flow_1.in_fluid.temperature - 273.15}\n" \
                  f"Fluid 2:{self.flow_2.in_fluid.temperature - 273.15}\n"
        output += f"Outputs: \n" \
                  f"Fluid 1:{self.flow_1.out_fluid.temperature - 273.15}\n" \
                  f"Fluid 2:{self.flow_2.out_fluid.temperature - 273.15}\n"
        output += self.dimensionless_parameters_str()
        return output

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
        p1 = (1 - exp(n1 * (r1 - 1))) / (1 - r1 * exp(n1 * (r1 - 1)))
        p2 = (1 - exp(n2 * (r2 - 1))) / (1 - r2 * exp(n2 * (r2 - 1)))
        return p1, p2


class CrossFlowOneRow(HeatExchanger):
    @property
    def p(self):
        n1, n2 = self.ntu
        r1, r2 = self.r
        p1 = 1 - exp((exp(-r1 * n1) - 1) / r1)
        p2 = 1 - exp((exp(-r2 * n2) - 1) / r2)
        return p1, p2


if __name__ == "__main__":
    print("Exchanger Test:")
    flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
    flow_2 = Flow(Fluid("Air"), 1)
    # ex = HeatExchanger(flow_1, flow_2, 10, 56)
    ex = ParallelFlow(flow_1, flow_2, 10, 56)
    ex.flow_1.out_fluid.temperature = 273.15 + 23.11
    print(ex.repr_short())
    # print(ex.r)
    # print(ex.str_r())
    # print(ex.p)
    # print(ex.str_p())
    # ex.heat_transferability = 50
    # print(ex.heat_transferability)
