from stream import Fluid, Flow
from numpy import exp


class HeatExchanger:
    def __init__(self, flow_1=None, flow_2=None, heat_transfer_area: float = None,
                 heat_transfer_coefficient: float = None):
        self._flow_1 = flow_1
        self._flow_2 = flow_2
        self._heat_transfer_area = heat_transfer_area
        self._heat_transfer_coefficient = heat_transfer_coefficient
        self._heat_transferability = None
        self._ntu = None
        self._r = None

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
    def heat_transfer_area(self):
        value = self._heat_transfer_area
        if value is None:
            raise NotImplementedError
        else:
            return value

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        self._heat_transfer_area = value

    @property
    def heat_transfer_coefficient(self):
        value = self._heat_transfer_coefficient
        if value is None:
            raise NotImplementedError
        else:
            return value

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        self._heat_transfer_coefficient = value

    @property
    def heat_transferability(self):
        value = self._heat_transferability
        if value is None:
            value = self.heat_transfer_area * self.heat_transfer_coefficient
        # @TODO implement Error handling
        return value

    @heat_transferability.setter
    def heat_transferability(self, value):
        self._heat_transferability = value

    @property
    def ntu(self):
        kA = self.heat_transferability
        heat_capacity_flow_1 = self.flow_1.get_heat_capacity_flow()
        heat_capacity_flow_2 = self.flow_2.get_heat_capacity_flow()
        if (kA and heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            ntu1 = kA / heat_capacity_flow_1
            ntu2 = kA / heat_capacity_flow_2
        return ntu1, ntu2

    def str_ntu(self):
        try:
            return f"NTU-Werte:\nNTU_1 = %.3f\nNTU_2 = %.3f\n" % (self.ntu)
        except TypeError:
            raise NotImplementedError

    @property
    def r(self):
        heat_capacity_flow_1 = self.flow_1.get_heat_capacity_flow()
        heat_capacity_flow_2 = self.flow_2.get_heat_capacity_flow()
        if (heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            r1 = heat_capacity_flow_1 / heat_capacity_flow_2
            r2 = heat_capacity_flow_2 / heat_capacity_flow_1
        return r1, r2

    def str_r(self):
        try:
            return f"Wärmekapazitätsstromverhältnisse:\nR_1 = %.3f\nR_2 = %.3f\n" % (self.r)
        except TypeError:
            raise NotImplementedError

    def __repr__(self) -> str:
        output = "Wärmeübertrager:\n"
        output += "\tFluids:\n" \
                  f"\tFluid 1:{self.flow_1}\n" \
                  f"\tFluid 2:{self.flow_2}\n"
        output += "\tParameters:\n" \
                  f"\theat_transferability: {self.heat_transferability:.2f} W/K"
        # output += f"Typ: {self.__class__.__name__}\n\n"
        # output += self.str_temperatures()
        # output += "\n" + self.str_dimensionless_parameters()
        return output


"""
    def set_part(self, part: Part):
        self.__part = part
        return self

    def get_part(self):
        return self.__part


    def get_r(self) -> tuple:
        r1 = r(self.get_flow_1().get_heat_capacity_flow(), self.get_flow_2().get_heat_capacity_flow())
        r2 = 1 / r1
        return r1, r2

    def str_r(self):
        try:
            return f"Wärmekapazitätsstromverhältnisse:\nR_1 = %.3f\nR_2 = %.3f\n" % (self.get_r())
        except TypeError:
            raise NotImplementedError

    def get_p(self) -> tuple:
        pass

    def str_p(self):
        try:
            return f"dimensionslose Temperaturänderungen:\nP_1 = %.3f\nP_2 = %.3f\n" % (self.get_p())
        except TypeError:
            raise NotImplementedError

    def str_dimensionless_parameters(self):
        return f"Dimensionslose Parameter:\n" + self.str_ntu() + self.str_r() + self.str_p()

    def __set_input_temperature(self, theta_1_1, theta_2_1):
        self.__theta_1_1 = theta_1_1
        self.__theta_2_1 = theta_2_1
        return self

    def get_input_temperature(self):
        return self.__theta_1_1, self.__theta_2_1

    def get_output_temperature(self):
        p1, p2 = self.get_p()
        theta_1_1, theta_2_1 = self.get_input_temperature()
        theta_1_2 = -(p1 * (theta_1_1 - theta_2_1) - theta_1_1)
        theta_2_2 = p2 * (theta_1_1 - theta_2_1) + theta_2_1
        return theta_1_2, theta_2_2

    def str_temperatures(self):
        fluid1, fluid2 = self.get_flow_1().fluid.name, self.get_flow_2().fluid.name
        theta_1_1, theta_2_1 = self.get_input_temperature()
        theta_1_2, theta_2_2 = self.get_output_temperature()
        output = f"Fluidtemperaturen:\n"
        output += f"Fluid %s: \nEintritt: {theta_1_1}Austritt: {theta_1_2}\n" % (fluid1)
        output += f"Fluid %s: \nEintritt: {theta_2_1}Austritt: {theta_2_2}\n" % (fluid2)
        return output




def ntu(heat_transferability, heat_capacity_flow):
    return heat_transferability / heat_capacity_flow


def p(theta_1_1, theta_1_2, theta_2_1, theta_2_2):
    p1 = (theta_1_1 - theta_1_2) / (theta_1_1 - theta_2_1)
    p2 = (theta_2_2 - theta_2_1) / (theta_1_1 - theta_2_1)
    return p1, p2


def r(heat_capacity_flow_1, heat_capacity_flow_2):
    return heat_capacity_flow_1 / heat_capacity_flow_2


class ParallelFlow(HeatExchanger):
    def get_p(self):
        n1, n2 = self.get_ntu()
        r1, r2 = self.get_r()
        p1 = (1 - exp(-n1 * (1 + r1))) / (1 + r1)
        p2 = (1 - exp(-n2 * (1 + r2))) / (1 + r2)
        return p1, p2


class CountercurrentFlow(HeatExchanger):
    def get_p(self):
        n1, n2 = self.get_ntu()
        r1, r2 = self.get_r()
        p1 = (1 - exp(n1 * (r1 - 1))) / (1 - r1 * exp(n1 * (r1 - 1)))
        p2 = (1 - exp(n2 * (r2 - 1))) / (1 - r2 * exp(n2 * (r2 - 1)))
        return p1, p2
"""

if __name__ == "__main__":
    print("Exchanger Test:")
    flow_1 = Flow(Fluid("Water"), 2)
    flow_2 = Flow(Fluid("Air"), 1)
    ex = HeatExchanger(flow_1, flow_2, 10, 56)
    print(ex)
    print(ex.r)
    print(ex.str_r())
    # ex.heat_transferability = 50
    # print(ex.heat_transferability)
