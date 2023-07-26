import numpy as np
from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow


class Network:
    def __init__(self):
        self._exchangers = []
        self._inputs = []
        self._outputs = []

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

        phi_1 = np.zeros(shape)
        phi_2 = np.zeros(shape)
        identity = np.eye(dim)

        for i, ex in enumerate(self.exchangers):
            phi_1[i, i], phi_2[i, i] = ex.p
        phi = np.block([[identity - phi_1, phi_1], [phi_2, identity - phi_2]])
        return phi

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
    kA = 4749/4
    W = 3500
    fld = Fluid("Water")
    flow = Flow(fld, W/fld.get_specific_heat())
    print(flow.str_heat_capacity_flow())
    ex = ParallelFlow(flow,flow)
    ex.heat_transferability = kA
    print(ex)
    netw = Network()
    netw.exchangers = [ex, ex,ex,ex]
    print(netw)
    phi = netw.phi
    print(phi)
