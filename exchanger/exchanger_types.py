import copy

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

    def paths(self, order_1, order_2):
        path_1 = self.flatten(order_1)
        path_1.insert(0, self.flow_1)
        out_1 = flow_1.copy()
        path_1.append(out_1)

        nodes = path_1

        tuples_list_1 = [(path_1[i], path_1[i + 1]) for i in range(len(path_1) - 1)]

        path_2 = self.flatten(order_2)
        path_2.insert(0, self.flow_2)
        nodes.insert(1, self.flow_2)
        out_2 = flow_2.copy()
        path_2.append(out_2)
        nodes.append(out_2)
        tuples_list_2 = [(path_2[i], path_2[i + 1]) for i in range(len(path_2) - 1)]
        return nodes, tuples_list_1, tuples_list_2

    def __repr__(self):
        output = f"Network:\ncell numbers={self.cell_numbers}\n"
        for i, ex in enumerate(self.exchangers.flatten()):
            output += f"\ncell:{i}\n{ex.repr_short()}\n"
        return output


def id_repr(matrix):
    vectorized_get_id = np.vectorize(lambda obj: obj.id)
    output = vectorized_get_id(matrix)
    return output


def matrix_repr(nodes, path_1,path_2):
    G1 = nx.DiGraph()
    G1.add_nodes_from(nodes)
    G1.add_edges_from(path_1)
    ad_1 = nx.adjacency_matrix(G1, nodelist=nodes).todense()
    print(ad_1)
    S11 = ad_1[2:-2, 2:-2]
    print(S11)
    Inp1 = ad_1[:2, 2:-2]
    print(Inp1)
    Out1 = ad_1[2:-2, -2:]
    print(Out1)

    G2 = nx.DiGraph()
    G2.add_nodes_from(nodes)
    G2.add_edges_from(path_2)
    ad_2 = nx.adjacency_matrix(G2, nodelist=nodes).todense()
    print(ad_2)
    S22 = ad_2[2:-2, 2:-2]
    print(S22)
    Inp2 = ad_2[:2, 2:-2]
    print(Inp2)
    Out2 = ad_2[2:-2, -2:]
    print(Out2)


if __name__ == "__main__":
    kA = 4749
    W = 3500
    fld_1 = Fluid("Water", temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.get_specific_heat())
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.get_specific_heat())

    sh = ShellTube((2, 2), flow_1, flow_2)
    sh.transferability = kA
    sh.fill('CrossFlowOneRow')
    # print(sh)
    print(id_repr(sh.exchangers))
    flat = sh.flatten('ur2d')
    # print(id_repr(flat))
    # print(flat)
    nodes, path_1, path_2 = sh.paths('ur2d', 'dl2r')
    print(id_repr(nodes))
    # print(id_repr(path_1))
    matrix_repr(nodes,path_1,path_2)