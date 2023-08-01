import copy

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow, CrossFlowOneRow
from matrix_converter import *
from numpy.linalg import inv


class Layout:

    def __init__(self, shape, flow_1, flow_2, transferability: float = None):
        self.layout = shape
        self.flow_1 = flow_1
        self.flow_2 = flow_2
        self.transferability = transferability
        self.order_1 = 'dl2r'
        self.order_2 = 'ur2d'

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, shape):
        if isinstance(shape, tuple):
            self._layout = np.zeros(shape, dtype=HeatExchanger)
        else:
            raise NotImplementedError

    @property
    def cell_numbers(self):
        value = self.layout.size
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

    def fill(self, ex_type: str = 'HeatExchanger', order: str = 'equal'):
        """
        fills the Layout with Heat Exchanger objects
        :param ex_type: type of HeatExchanger (must be implemented in exchangers)
        :param order: if equal, all cells are same heat Exchanger type,
                        transferability is divided equal by number of cells
        """
        if order == 'equal':
            ex_class = globals()[ex_type]

            for i in range(self.layout.shape[0]):
                for j in range(self.layout.shape[1]):
                    ex = ex_class(self.flow_1, self.flow_2)
                    ex.heat_transferability = self.transferability / self.cell_numbers
                    self.layout[i, j] = ex
        else:
            pass

    @property
    def nodes(self):
        try:
            value = self._nodes
        except AttributeError:
            self._extract_node_paths()
            value = self._nodes
        return value

    @property
    def paths(self):
        try:
            value = self._paths
        except AttributeError:
            self._extract_node_paths()
            value = self._paths
        return value

    @property
    def order_1(self):
        return self._order_1

    @order_1.setter
    def order_1(self, value: str):
        self._order_1 = value

    @property
    def order_2(self):
        return self._order_2

    @order_2.setter
    def order_2(self, value: str):
        self._order_2 = value

    def _extract_node_paths(self, order_1: str = None, order_2: str = None):
        if order_1 is not None: self.order_1 = order_1
        if order_2 is not None: self.order_2 = order_2

        path_1 = flatten(self.layout, self.order_1)
        path_1.insert(0, self.flow_1)
        out_1 = flow_1.copy()
        path_1.append(out_1)

        nodes = path_1

        tuples_list_1 = list_2_tuplelist(path_1)

        path_2 = flatten(self.layout, self.order_2)
        path_2.insert(0, self.flow_2)
        nodes.insert(1, self.flow_2)
        out_2 = flow_2.copy()
        path_2.append(out_2)
        nodes.append(out_2)

        tuples_list_2 = list_2_tuplelist(path_2)

        self._nodes = nodes
        self._paths = tuples_list_1, tuples_list_2

    @property
    def adjacency(self):
        try:
            value = self._adj_1, self._adj_2
        except AttributeError:
            self._matrix_representation()
            value = self._adj_1, self._adj_2
        return value

    def _matrix_representation(self):
        nodes = self._nodes
        path_1, path_2 = self.paths

        graph_1 = nx.DiGraph()
        graph_1.add_nodes_from(nodes)
        graph_1.add_edges_from(path_1)
        adj_1 = nx.adjacency_matrix(graph_1, nodelist=nodes).todense()

        graph_2 = nx.DiGraph()
        graph_2.add_nodes_from(nodes)
        graph_2.add_edges_from(path_2)
        adj_2 = nx.adjacency_matrix(graph_2, nodelist=nodes).todense()

        self._adj_1 = adj_1
        self._adj_2 = adj_2

    @property
    def structure_matrix(self):
        s11 = self.adjacency[0][2:-2, 2:-2]
        s22 = self.adjacency[1][2:-2, 2:-2]
        zeros = np.zeros_like(s11)
        structure = np.block([[s11, zeros], [zeros, s22]])
        return structure

    @property
    def input_matrix(self):
        in_1 = self.adjacency[0][:2, 2:-2]
        in_2 = self.adjacency[1][:2, 2:-2]
        input = np.hstack((in_1, in_2))
        return input

    @property
    def output_matrix(self):
        out_1 = self.adjacency[0][2:-2, -2:]
        out_2 = self.adjacency[1][2:-2, -2:]
        output = np.vstack((out_1, out_2))
        return output

    @property
    def temperature_input_matrix(self):
        temp_1 = flow_1.mean_fluid.temperature
        temp_2 = flow_2.mean_fluid.temperature
        if temp_1 >= temp_2:
            return np.matrix([[1], [0]])
        else:
            return np.matrix([[0], [1]])

    @property
    def phi_matrix(self):
        exchangers = self.nodes[2:-2]
        dim = len(exchangers)
        shape = (dim, dim)

        phi_1 = np.zeros(shape)
        phi_2 = np.zeros(shape)
        identity = np.eye(dim)

        for i, ex in enumerate(exchangers):
            phi_1[i, i], phi_2[i, i] = ex.p
        value = np.block([[identity - phi_1, phi_1], [phi_2, identity - phi_2]])
        return value

    @property
    def temperatures(self):
        phi = self.phi_matrix
        s = self.structure_matrix
        inp = self.input_matrix
        ti = self.temperature_input_matrix

        ps = phi @ s
        identity = np.eye(ps.shape[0])

        value = inv((identity - ps)) @ phi @ inp @ ti
        return value

    def __repr__(self):
        output = f"Network:\ncell numbers={self.cell_numbers}\n"
        for i, ex in enumerate(self.layout.flatten()):
            output += f"\ncell:{i}\n{ex.repr_short()}\n"
        return output


if __name__ == "__main__":
    kA = 4749
    W = 3500
    fld_1 = Fluid("Water", temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.get_specific_heat())
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.get_specific_heat())

    sh = Layout((2, 2), flow_1, flow_2)
    sh.transferability = kA
    sh.fill('CrossFlowOneRow')
    # print(sh)
    print(id_repr(sh.layout))
    # sh._extract_node_paths('ur2d', 'dl2r')
    print(id_repr(sh.nodes))
    print(id_repr(sh.paths[0]))
    # print(sh.adjacency[1])
    print(sh.structure_matrix)
    print(sh.input_matrix)
    print(sh.output_matrix)
    print(sh.phi_matrix)
    print(sh.temperatures)
    # matrix_repr(nodes, path_1, path_2)
    # @TODO check why output shapes a transposed