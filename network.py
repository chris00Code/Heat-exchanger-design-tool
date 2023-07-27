import numpy as np

from numpy.linalg import inv

from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow


class Network:
    def __init__(self):
        self._exchangers = []
        # self._inputs = []
        # self._outputs = []
        # self._paths = []
        # self._structure = None

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
    def phi(self):
        dim = len(self.exchangers)
        shape = (dim, dim)

        if dim != 0:
            phi_1 = np.zeros(shape)
            phi_2 = np.zeros(shape)
            identity = np.eye(dim)

            for i, ex in enumerate(self.exchangers):
                phi_1[i, i], phi_2[i, i] = ex.p
            self._phi = np.block([[identity - phi_1, phi_1], [phi_2, identity - phi_2]])
        return self._phi

    @phi.setter
    def phi(self, value):
        if len(self.exchangers) != 0:
            raise ValueError("exchangers already implemented")
        elif isinstance(value, np.matrix):
            self._phi = value
        else:
            raise NotImplementedError

    @property
    def structure(self):
        try:
            value = self._structure
        except AttributeError:
            value = None
        return value

    @structure.setter
    def structure(self, value):
        # @TODO implement graph converting
        if isinstance(value, np.matrix):
            self._structure = value
        else:
            raise NotImplementedError

    @property
    def input(self):
        try:
            value = self._input
        except AttributeError:
            value = None
        return value

    @input.setter
    def input(self, value):
        # @TODO implement graph converting
        if isinstance(value, np.matrix):
            self._input = value
        else:
            raise NotImplementedError

    @property
    def temperature_inputs(self):
        try:
            value = self._temperature_inputs
        except AttributeError:
            value = None
        return value

    @temperature_inputs.setter
    def temperature_inputs(self, value):
        # @TODO implement graph converting
        if isinstance(value, np.matrix):
            self._temperature_inputs = value
        else:
            raise NotImplementedError

    @property
    def temperatures(self):
        phi = self.phi
        s = self.structure
        inp = self.input
        ti = self.temperature_inputs

        ps = phi @ s
        identity = np.eye(ps.shape[0])

        self._temperatures = inv((identity - ps)) @ phi @ inp @ ti
        return self._temperatures

    @property
    def outputs(self):
        try:
            value = self._outputs
        except AttributeError:
            value = None
        return value

    @outputs.setter
    def outputs(self, value):
        # @TODO implement graph converting
        if isinstance(value, np.matrix):
            self._outputs = value
        else:
            raise NotImplementedError
    @property
    def temperature_outputs(self):
        value = self.outputs@self.temperatures
        return value

    def __repr__(self):
        output = "Heat Exchanger Network:\n"
        output += f"{self.exchangers}"
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