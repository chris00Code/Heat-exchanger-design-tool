import warnings

from numpy import exp, sqrt

from .stream import Fluid, Flow
from .parts import Part


class HeatExchanger:
    """
    A class representing a heat exchanger.

    Args:
        flow_1 (Flow, optional): The first fluid flow in the heat exchanger.
        flow_2 (Flow, optional): The second fluid flow in the heat exchanger.
        part (Part, optional): The heat exchanger component.

    Attributes:
        auto_adjust (bool): If output values should be adjusted for str representation
    """
    auto_adjust = True

    def __init__(self, flow_1=None, flow_2=None, part: Part = None):
        self.flow_1 = flow_1
        self.flow_2 = flow_2
        self.part = part

    @property
    def flow_1(self):
        """
        Get or set the first fluid flow in the heat exchanger.

        Args:
            value (Flow): The first fluid flow.

        Raises:
            NotImplementedError: If the provided value is not a Flow.

        """
        return self._flow_1

    @flow_1.setter
    def flow_1(self, value):
        if isinstance(value, Flow):
            self._flow_1 = value
        else:
            raise NotImplementedError

    @property
    def flow_2(self):
        """
        Get or set the second  fluid flow in the heat exchanger.

        Args:
            value (Flow): The second fluid flow.

        Raises:
            NotImplementedError: If the provided value is not a Flow.

        """
        return self._flow_2

    @flow_2.setter
    def flow_2(self, value):
        if isinstance(value, Flow):
            self._flow_2 = value
        else:
            raise NotImplementedError

    @property
    def part(self):
        """
        Get or set the heat exchanger component.

        Args:
            value (Part): The new heat exchanger component.

        """
        return self._part

    @part.setter
    def part(self, value):
        if value is None:
            value = Part()
        self._part = value

    @property
    def heat_transfer_area(self):
        """
        Get or set the heat transfer area of the part in square meters (m^2).

        Args:
            value (float): The new heat transfer area to set in square meters (m^2).

        Returns:
            float: The heat transfer area of the part in square meters (m^2).
        """
        return self.part.heat_transfer_area

    @heat_transfer_area.setter
    def heat_transfer_area(self, value):
        self.part.heat_transfer_area = value

    @property
    def heat_transfer_coefficient(self):
        """
        Get or set the heat transfer coefficient of the part in W/(m^2 K).

        Args:
            value (float): The new heat transfer coefficient to set in W/(m^2 K).

        Returns:
            float: The heat transfer coefficient of the part in W/(m^2 K).
        """
        return self.part.heat_transfer_coefficient

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value):
        self.part.heat_transfer_coefficient = value

    @property
    def heat_transferability(self):
        """
        Get or set the heat transferability of the part in W/K.

        Args:
            value (float): The new heat transferability to set in W/K.

        Returns:
            float: The heat transferability of the part in W/K.
        """
        return self.part.heat_transferability

    @heat_transferability.setter
    def heat_transferability(self, value):
        self.part.heat_transferability = value

    @property
    def heat_capacity_flow(self):
        """
        Get the heat capacity flow of the heat exchanger.

        Returns:
            tuple (float, float): A tuple containing the heat capacity flow of the first and second fluid flows.

        """
        return self.flow_1.heat_capacity_flow, self.flow_2.heat_capacity_flow

    @property
    def heat_flows(self):
        """
        Get the heat flows of the heat exchanger.

        Returns:
            tuple (float, float): A tuple containing the heat flow of the first and second fluid flows.

        """
        return self.flow_1.heat_flow, self.flow_2.heat_flow

    @property
    def pressure_loss(self):
        """
        Calculate the pressure loss of the two fluids in the heat exchanger.

        Returns:
            float: The pressure loss.

        Notes:
            This method calculates the pressure loss based on the heat exchanger's parameters.
            flow 1 is assumed as the flow inside the part.

        """
        # TODO calculation not implemented
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
        """
        Calculate the pressure loss in the heat exchanger.

        Args:
            zeta (float): Pressure coefficient.
            velocity (float): Fluid velocity.
            density (float): Fluid density.

        Returns:
            float: The calculated pressure loss.

        Notes:
            This method calculates the pressure loss based on the provided pressure coefficient, fluid velocity, and fluid density.

        """
        return zeta * density / 2 * velocity ** 2

    def _calc_output(self, n_iter: int = 5):
        """
        Calculate the output temperatures of the heat exchanger.

        Args:
            n_iter (int): number of iterations

        Notes:
            This method calculates the output temperatures of the fluid flows in the heat exchanger based on the
            dimensionless temperature change (P) of the heat exchanger.
            The temperature and thus the fluid properties, are iteratively adjusted n_iter times to find stable output temperatures.
        """
        for i in range(n_iter):
            temp_1_in = self.flow_1.in_fluid.temperature
            temp_2_in = self.flow_2.in_fluid.temperature
            p1, p2 = self.p
            temp_1_out = -p1 * (temp_1_in - temp_2_in) + temp_1_in
            temp_2_out = p2 * (temp_1_in - temp_2_in) + temp_2_in
            self.flow_1.out_temperature = temp_1_out
            self.flow_2.out_temperature = temp_2_out

    @property
    def ntu(self):
        """
        Get the number of transfer units (NTU) of the heat exchanger.

        Returns:
            tuple (float, float): A tuple containing the NTU values for the first and second fluid flows.

        Notes:
            - The NTU values are calculated based on the heat exchanger's parameters.
            - NTU_1 represents the NTU value for one side, and NTU_2 for the other side.

        """
        kA = self.heat_transferability
        heat_capacity_flow_1 = self.flow_1.heat_capacity_flow
        heat_capacity_flow_2 = self.flow_2.heat_capacity_flow
        ntu1, ntu2 = NotImplemented, NotImplemented
        if kA is not NotImplemented and (heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            ntu1 = kA / heat_capacity_flow_1
            ntu2 = kA / heat_capacity_flow_2
        return ntu1, ntu2

    def ntu_str(self):
        """
        Return a formatted string for the number of transfer units (NTU) of the heat exchanger.

        Returns:
            str: A string containing the NTU values of the heat exchanger.

        """
        output = "number of transfer units:\n"
        try:
            output += f"\tNTU_1 = %.3f\n\tNTU_2 = %.3f\n" % (self.ntu)
        except TypeError:
            output += "\tNot implemented\n"
        return output

    @property
    def r(self):
        """
        Get the heat capacity flow ratios of the heat exchanger.

        Returns:
            tuple (float, float): A tuple containing the heat capacity flow ratios for the first and second fluid flows.

        Raises:
            ValueError: If heat capacity flow values are not defined.

        Notes:
            - The heat capacity flow ratios are calculated based on the heat exchanger's parameters.
            - R_1 represents the heat capacity flow ratio for one side, and R_2 for the other side.

        """
        heat_capacity_flow_1 = self.flow_1.heat_capacity_flow
        heat_capacity_flow_2 = self.flow_2.heat_capacity_flow
        if (heat_capacity_flow_1 and heat_capacity_flow_2) is not None:
            r1 = heat_capacity_flow_1 / heat_capacity_flow_2
            r2 = heat_capacity_flow_2 / heat_capacity_flow_1
        else:
            raise ValueError("heat capacity flow not defined")
        return r1, r2

    def r_str(self):
        """
        Return a formatted string for the heat capacity flow ratios of the heat exchanger.

        Returns:
            str: A string containing the heat capacity flow ratios of the heat exchanger.

        """
        output = "heat capacity flow ratios:\n"
        try:
            output += f"\tR_1 = %.3f\n\tR_2 = %.3f\n" % (self.r)
        except TypeError:
            output += "\tNot implemented\n"
        return output

    @property
    def p(self):
        """
        Get the dimensionless temperature change for a heat exchanger.

        Raises:
            NotImplementedError: If the dimensionless temperature change is required
            from a heat exchanger with no specific type.
        """
        pass
        raise NotImplementedError

    def p_str(self):
        """
        Return a formatted string for the dimensionless temperature of the heat exchanger.

        Returns:
            str: A string containing the dimensionless temperature of the heat exchanger.

        """
        output = "dimensionless temperature change:\n"
        try:
            output += f"\tP_1 = %.3f\n\tP_2 = %.3f\n" % (self.p)
        except TypeError:
            output += "\tNot implemented\n"
        except NotImplementedError:
            output += "\tnot defined for HeatExchanger"
        return output

    def dimensionless_parameters_str(self):
        """
        Return a formatted string for the dimensionless parameters of the heat exchanger.

        Returns:
            str: A string containing the str representations for number of transfer units (NTU),
             heat capacity flow ratios (R), and dimensionless temperature (P) of the heat exchanger.

        """
        return f"dimensionless parameters:\n" + self.ntu_str() + self.r_str() + self.p_str()

    def __repr__(self) -> str:
        if self.auto_adjust:
            self._calc_output()
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
        """
        Get the dimensionless temperature changes (P1 and P2) for a parallel flow heat exchanger.

        Returns:
            tuple (float,float): A tuple containing two dimensionless temperature changes, P1 and P2.

        Notes:
            - The dimensionless temperature changes are calculated based on the heat exchanger's NTU and R values.
            - P1 represents the dimensionless temperature change on one side, and P2 on the other side.
        """
        n1, n2 = self.ntu
        r1, r2 = self.r
        p1 = (1 - exp(-n1 * (1 + r1))) / (1 + r1)
        p2 = (1 - exp(-n2 * (1 + r2))) / (1 + r2)
        return p1, p2


class CounterCurrentFlow(HeatExchanger):
    @property
    def p(self):
        """
        Get the dimensionless temperature changes (P1 and P2) for a counter current flow heat exchanger.

        Returns:
            tuple (float,float): A tuple containing two dimensionless temperature changes, P1 and P2.

        Notes:
            - The dimensionless temperature changes are calculated based on the heat exchanger's NTU and R values.
            - P1 represents the dimensionless temperature change on one side, and P2 on the other side.
        """
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
        """
        Get the dimensionless temperature changes (P1 and P2) for a One-sided cross-mixed crossflow heat exchanger.

        Returns:
            tuple (float,float): A tuple containing two dimensionless temperature changes, P1 and P2.

        Notes:
            - The dimensionless temperature changes are calculated based on the heat exchanger's NTU and R values.
            - P1 represents the dimensionless temperature change of ideally mixed flow 1, and P2 not.
        """
        n1, n2 = self.ntu
        r1, r2 = self.r
        p1 = 1 - exp((exp(-r1 * n1) - 1) / r1)
        p2 = r1 * p1
        return p1, p2


class ShellTubeHeatExchanger(HeatExchanger):
    pass


class OneOuterThreeInnerTwoCounterFlow(ShellTubeHeatExchanger):
    @property
    def p(self):
        """
        Get the dimensionless temperature changes (P1 and P2) for a Shell-and-tube heat exchanger
        with one outer and three inner passages, two in counterflow.

        Returns:
            tuple (float,float): A tuple containing two dimensionless temperature changes, P1 and P2.

        Notes:
            - The dimensionless temperature changes are calculated based on the heat exchanger's NTU and R values.
            - P1 represents the dimensionless temperature change on the shell side, and P2 on the tube side.

            Formula: VDI Waermeatlas, C1 Wärmeübertrager: Berechnungsmethoden, Tab 5
        """
        n1, n2 = self.ntu
        r1, r2 = self.r
        # formula from VDI Waermeatlas
        epsilon = 1 / 3
        if r1 != 1:
            p = n1 * (1 - 1 / 2 * r1 * (1 - 3 * epsilon))
            q = 1 / 2 * epsilon * (1 - epsilon) * n1 ** 2 * r1 * (1 - r1)
            s1 = -p / 2 + sqrt(p ** 2 / 4 - q)
            s2 = -p / 2 - sqrt(p ** 2 / 4 - q)
            s3 = 1 / 2 * r1 * n1 * (1 - epsilon)

            p1 = (s1 * (exp(s1) + exp(s3)) * (exp(s2) - 1) +
                  s2 * (exp(s2) + exp(s3)) * (1 - exp(s1)) +
                  n1 * (1 - r1) * (exp(s2) - exp(s1)) * (1 + exp(s3))) / \
                 (s1 * (exp(s1) + exp(s3)) * (r1 * exp(s2) - 1) +
                  s2 * (exp(s2) + exp(s3)) * (1 - r1 * exp(s1)) +
                  n1 * (1 - r1) * (exp(s2) - exp(s1)) * (1 + r1 * exp(s3)))
        else:
            x = n1 * (epsilon * (1 - epsilon)) / (1 + 3 * epsilon) - 2 * ((1 + epsilon) / (1 + 3 * epsilon)) ** 2 * \
                ((exp(-0.5 * n1 * (1 + 3 * epsilon)) - 1) ** (-1) + (exp(0.5 * n1 * (1 - epsilon)) + 1) ** (-1)) ** (-1)
            p1 = x / (x + 1)
        p2 = r1 * p1

        return p1, p2
