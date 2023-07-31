import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow, CrossFlowOneRow


class ShellTube:

    def __init__(self, shape, flow_1, flow_2):
        self.exchangers = shape
        self.flow_1 = flow_1
        self.flow_2 = flow_2
        # self._transferability = None

    @property
    def exchangers(self):
        return self._exchangers

    @exchangers.setter
    def exchangers(self, value):
        if isinstance(value, tuple):
            self._exchangers = np.zeros(value, dtype=HeatExchanger)
        else:
            raise NotImplementedError

    @property
    def cell_numbers(self):
        value = self.exchangers.size
        return value

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
    def transferability(self):
        return self._transferability

    @transferability.setter
    def transferability(self, value):
        self._transferability = value

    def fill(self, ex_type=None):
        ex_class = globals()[ex_type]

        for i in range(self.exchangers.shape[0]):
            for j in range(self.exchangers.shape[1]):
                ex = ex_class(self.flow_1, self.flow_2)
                ex.heat_transferability = self.transferability / self.cell_numbers
                self.exchangers[i, j] = ex

    def flatten(self, order):
        flattened = []
        array = self.exchangers
        rows, cols = array.shape
        match order:
            case 'ul2r':  # beginning up left to right
                flattened = self._l2r(array)
            case 'dl2r':  # beginning down left to right
                flattened = self._l2r(np.flipud(array))
            case 'ul2d':
                flattened = self._l2r(array.T)
            case 'ur2d':
                flattened = self._l2r(np.flipud(array.T))
        return flattened

    @staticmethod
    def _l2r(array):
        flattened = []
        for i, row in enumerate(array):
            if i % 2 != 0:
                row = np.flip(row)
            for j, cell in enumerate(row):
                flattened.append(cell)
        return flattened

    def __repr__(self):
        output = f"Network:\ncell numbers={self.cell_numbers}\n"
        for i, ex in enumerate(self.exchangers.flatten()):
            output += f"\ncell:{i}\n{ex.repr_short()}\n"
        return output


def id_repr(matrix):
    vectorized_get_id = np.vectorize(lambda obj: obj.id)
    output = vectorized_get_id(matrix)
    return output


if __name__ == "__main__":
    kA = 4749
    W = 3500
    fld_1 = Fluid("Water", temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.get_specific_heat())
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.get_specific_heat())

    sh = ShellTube((4, 3), flow_1, flow_2)
    sh.transferability = kA
    sh.fill('CrossFlowOneRow')
    # print(sh)
    print(id_repr(sh.exchangers))
    flat = sh.flatten('ur2d')
    print(id_repr(flat))
    # print(flat)
    """
    ex = CrossFlowOneRow(flow_1, flow_2)
    ex.heat_transferability = kA / 4
    sh = ShellTube(flow_1, flow_2)
    sh.fill(ex)
    sh._exchangers[0, 0].flow_1._out_fluid.temperature = 400
    print(sh)
    """
