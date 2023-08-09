import numpy as np

from numpy.linalg import inv

from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow


class ExchangerNetwork:
    def __init__(self, input_flows: list = None, exchangers: list = None, output_flows: list = None):
        if input_flows is None:
            input_flows = list()
        self.input_flows = input_flows

        if exchangers is None:
            exchangers = list()
        self.exchangers = exchangers

        if output_flows is None:
            output_flows = list()
        self.output_flows = output_flows

        self._input_temps = [], None

    @property
    def input_flows(self):
        return self._input_flows

    @input_flows.setter
    def input_flows(self, value):
        if isinstance(value, list):
            self._input_flows = value
        else:
            raise NotImplementedError

    @property
    def exchangers(self):
        return self._exchangers

    @exchangers.setter
    def exchangers(self, value):
        if isinstance(value, list):
            self._exchangers = value
        elif isinstance(value, HeatExchanger):
            self._exchangers.append(value)

    @property
    def cell_numbers(self):
        value = self.exchangers.size
        return value

    @property
    def output_flows(self):
        return self._output_flows

    @output_flows.setter
    def output_flows(self, value):
        if isinstance(value, list):
            self._output_flows = value
        else:
            raise NotImplementedError

    @property
    def input_temps(self):
        value = self._input_temps
        if value[0] is None:  # only if input temps is set dirrectly
            return self._input_temps
        else:  # calculating input temps
            temps = []
            for flow in self.input_flows:
                temp = flow.mean_fluid.temperature
                temps.append(temp)
            if len(temps) != 0:
                dimensionless_matrix = np.asarray(temps, dtype=float)
                max_temp = max(temps)
                min_temp = min(temps)
                dimensionless_matrix = np.interp(dimensionless_matrix, (min_temp, max_temp), (0, 1))
                dimensionless_matrix = dimensionless_matrix.reshape((dimensionless_matrix.shape[0], 1))
            else:
                dimensionless_matrix = None
            self._input_temps = temps, dimensionless_matrix
        return self._input_temps

    @input_temps.setter
    def input_temps(self, value):
        if isinstance(value, np.ndarray):
            dimensionless_matrix = value
            temps = None
        else:
            raise NotImplementedError
        self._input_temps = temps, dimensionless_matrix

    @property
    def structure_matrix(self):
        try:
            return self._structure_matrix
        except AttributeError:
            pass

    @structure_matrix.setter
    def structure_matrix(self, value):
        if isinstance(value, np.ndarray):
            self._structure_matrix = value
        else:
            raise NotImplementedError

    @property
    def input_matrix(self):
        try:
            return self._input_matrix
        except AttributeError:
            pass

    @input_matrix.setter
    def input_matrix(self, value):
        if isinstance(value, np.ndarray):
            self._input_matrix = value
        else:
            raise NotImplementedError

    @property
    def output_matrix(self):
        try:
            return self._output_matrix
        except AttributeError:
            pass

    @output_matrix.setter
    def output_matrix(self, value):
        if isinstance(value, np.ndarray):
            self._output_matrix = value
        else:
            raise NotImplementedError

    @property
    def temperature_input_matrix(self):
        return self.input_temps[1]

    @property
    def phi_matrix(self):
        try:
            value = self._phi_matrix
        except AttributeError:
            exchangers = self.exchangers
            dim = len(exchangers)
            shape = (dim, dim)

            phi_1 = np.zeros(shape)
            phi_2 = np.zeros(shape)
            identity = np.eye(dim)

            for i, ex in enumerate(exchangers):
                phi_1[i, i], phi_2[i, i] = ex.p
            value = np.block([[identity - phi_1, phi_1], [phi_2, identity - phi_2]])
        return value

    @phi_matrix.setter
    def phi_matrix(self, value):
        if isinstance(value, np.ndarray):
            self._phi_matrix = value
        else:
            raise NotImplementedError

    @property
    def temperature_matrix(self):
        phi = self.phi_matrix
        s = self.structure_matrix
        inp = self.input_matrix
        ti = self.temperature_input_matrix

        ps = phi @ s
        identity = np.eye(ps.shape[0])

        value = inv((identity - ps)) @ phi @ inp @ ti
        return value, self._dimles_2_temp(value)

    def _dimles_2_temp(self, matrix):
        temps = self.input_temps[0]
        min_temp = min(temps)
        max_temp = max(temps)
        return (max_temp - min_temp) * matrix + min_temp

    @property
    def temperature_outputs(self):
        value = self.output_matrix @ self.temperature_matrix[0]
        return value, self._dimles_2_temp(value)

    def __repr__(self):
        output = "Heat Exchanger Network:\n"
        output += f"\tcell numbers: {self.cell_numbers}\n"
        for i, ex in enumerate(self.exchangers):
            output += f"\ncell:{i}\n{ex}\n"
        return output


if __name__ == "__main__":
    """
    flow_1 = Flow(Fluid("Water"), 2)
    flow_2 = Flow(Fluid("Air"), 1)
    flow_3 = Flow(Fluid("Acetone"), 5)
    flow_4 = Flow(Fluid("Water"), 10)
    ex1 = ParallelFlow(flow_1, flow_2, 10, 5)
    ex2 = CounterCurrentFlow(flow_3, flow_4, 5, 200)
    netw = Network()
    netw.exchangers = [ex1, ex2]
    print(netw)
    phi = netw.phi
    print(phi)
    """
    """
    kA = 4749 / 4
    W = 3500
    fld = Fluid("Water")
    flow = Flow(fld, W / fld.get_specific_heat())
    print(flow.str_heat_capacity_flow())
    ex = ParallelFlow(flow, flow)
    ex.heat_transferability = kA
    print(ex)
    netw = Network()
    netw.exchangers = [ex, ex, ex, ex]
    print(netw)
    phi = netw.phi
    print(phi)
    """
    """
    phi = np.matrix([[0.75, 0., 0., 0., 0.25, 0., 0., 0.],
                     [0., 0.75, 0., 0., 0., 0.25, 0., 0.],
                     [0., 0., 0.75, 0., 0., 0., 0.25, 0.],
                     [0., 0., 0., 0.75, 0., 0., 0., 0.25],
                     [0.25, 0., 0., 0., 0.75, 0., 0., 0.],
                     [0., 0.25, 0., 0., 0., 0.75, 0., 0.],
                     [0., 0., 0.25, 0., 0., 0., 0.75, 0.],
                     [0., 0., 0., 0.25, 0., 0., 0., 0.75]])
    netw = Network()
    netw.phi = phi
    netw.structure = np.matrix([[0., 1., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 1., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0.],
                                [1., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 1., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 1., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 1., 0.]])
    netw.input = np.matrix([[0, 0],
                            [0, 0],
                            [1, 0],
                            [0, 0],
                            [0, 1],
                            [0, 0],
                            [0, 0],
                            [0, 0]])
    netw.temperature_inputs = np.matrix([[1], [0]])
    print(netw.temperatures)
    netw.outputs = np.matrix([[0, 0, 0, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 1]])
    print(netw.temperature_outputs)
    """
