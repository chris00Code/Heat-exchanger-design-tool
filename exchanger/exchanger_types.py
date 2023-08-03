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
        self.input_temps = None
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

    @property
    def input_temps(self):
        return self._input_temps

    @input_temps.setter
    def input_temps(self, value):
        if value is not None:
            raise NotImplementedError
        else:
            temp_1 = flow_1.mean_fluid.temperature
            temp_2 = flow_2.mean_fluid.temperature
            if temp_1 >= temp_2:
                dimles_matrix = np.matrix([[1], [0]])
            else:
                dimles_matrix = np.matrix([[0], [1]])
        self._input_temps = temp_1, temp_2, dimles_matrix

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
                    ex = ex_class(self.flow_1.copy(), self.flow_2.copy())
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

        ex_path_1 = flatten(self.layout, self.order_1)
        path_1 = ex_path_1.copy()
        path_1.insert(0, self.flow_1)
        out_1 = flow_1.copy()
        path_1.append(out_1)

        nodes = path_1.copy()

        tuples_list_1 = list_2_tuplelist(path_1)

        ex_path_2 = flatten(self.layout, self.order_2)
        path_2 = ex_path_2.copy()
        path_2.insert(0, self.flow_2)
        nodes.insert(1, self.flow_2)
        out_2 = flow_2.copy()
        path_2.append(out_2)
        nodes.append(out_2)

        tuples_list_2 = list_2_tuplelist(path_2)

        self._nodes = nodes
        self.exchangers_flattened = (ex_path_1, ex_path_2)
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
        structure = np.block([[s11, zeros], [zeros, s22]]).T
        return structure

    @property
    def input_matrix(self):
        in_1 = self.adjacency[0][:2, 2:-2]
        in_2 = self.adjacency[1][:2, 2:-2]
        input = np.hstack((in_1, in_2)).T
        return input

    @property
    def output_matrix(self):
        out_1 = self.adjacency[0][2:-2, -2:]
        out_2 = self.adjacency[1][2:-2, -2:]
        output = np.vstack((out_1, out_2)).T
        return output

    @property
    def temperature_input_matrix(self):
        return self.input_temps[2]

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
    def temperature_matrix(self):
        phi = self.phi_matrix
        s = self.structure_matrix
        inp = self.input_matrix
        ti = self.temperature_input_matrix

        ps = phi @ s
        identity = np.eye(ps.shape[0])

        value = inv((identity - ps)) @ phi @ inp @ ti
        return value, self._dimles_2_temp(value)

    @property
    def temperature_outputs(self):
        value = self.output_matrix @ self.temperature_matrix[0]
        return value, self._dimles_2_temp(value)

    def _dimles_2_temp(self, matrix):
        temp_1, temp_2, _ = self.input_temps
        return (temp_1 - temp_2) * matrix + temp_2

    """@property
    def cell_temperatures_input(self):
        # @TODO implement S11, S22 in property method
        # @TODO check why temp input 1 wrong
        temp_1 = self.adjacency[0][2:-2, 2:-2].T @ self.temperature_matrix[0][:4]
        temp_2 = self.adjacency[1][2:-2, 2:-2].T @ self.temperature_matrix[0][4:]
        value = (temp_1, temp_2)
        dimles = (self._dimles_2_temp(temp_1), self._dimles_2_temp(temp_2))
        return value, dimles"""

    def _adjust_temperatures(self):
        """
        cell_out_temps = self.temperature_matrix[1]
        in_1, in_2, _ = self.input_temps

        n = self.temperature_matrix[0].shape[0] // 2
        # cell_out_2 = self._dimles_2_temp(self.adjacency[1][2:-2, 2:-2].T @ self.temperature_matrix[0][n:])
        out_2 = self.temperature_outputs[1][1][0, 0]

        temps_1 = [in_1] + cell_out_temps[:n].flatten().tolist()[0]
        # temps_2 = [in_2]+cell_out_temps[4:].flatten().tolist()[0]
        temps_2 = [in_2] + cell_out_temps[n:].flatten().tolist()[0] + [out_2]
        exchangers = self.nodes[2:-2]
        for i, ex in enumerate(exchangers):
            ex.flow_1.in_fluid.temperature = temps_1[i]
            ex.flow_2.in_fluid.temperature = temps_2[i]
            ex.flow_1.out_fluid.temperature = temps_1[i + 1]
            ex.flow_2.out_fluid.temperature = temps_2[i + 1]
        """
        cell_out_temps = self.temperature_matrix[1].flatten().tolist()[0]
        n = len(cell_out_temps) // 2

        exchangers_flattened_1, exchangers_flattened_2 = self.exchangers_flattened
        # for i, ex in enumerate(self.nodes[2:-2]):
        for i, ex in enumerate(exchangers_flattened_1):
            # adjust out temps
            ex.flow_1.out_fluid.temperature = cell_out_temps[i]
            ex.flow_2.out_fluid.temperature = cell_out_temps[n + i]

            # adjust in temp 1
            if i > 0:
                ex.flow_1.in_fluid.temperature = cell_out_temps[i - 1]

        # adjust in temp 2
        for i, ex in enumerate(exchangers_flattened_2):
            if i > 0:
                ex.flow_2.in_fluid.temperature = prev_out_temp
            prev_out_temp = ex.flow_2.out_fluid.temperature

    @property
    def heat_flows(self):
        q_1, q_2 = 0, 0
        for row in self.layout:
            for ex in row:
                q_1 += ex.heat_flows[0]
                q_2 += ex.heat_flows[1]
        return q_1, q_2

    def __repr__(self):
        output = f"Network:\ncell numbers={self.cell_numbers}\n"
        for i, ex in enumerate(self.layout.flatten()):
            output += f"\ncell:{i}\n{ex.repr_short()}\n"
        return output


if __name__ == "__main__":
    kA = 4000
    W = 3500
    fld_1 = Fluid("Water", pressure=101420 ,temperature=373.15)
    print(fld_1)
    flow_1 = Flow(fld_1, W / fld_1.get_specific_heat())
    #flow_1 = Flow(fld_1, 1.683)
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.get_specific_heat())
    #flow_2 = Flow(fld_2, 0.837)

    sh = Layout((2, 2), flow_1, flow_2)
    sh.transferability = kA
    sh.fill('CrossFlowOneRow')
    # print(sh)
    sh.order_1 = 'dr2u'
    sh.order_2 = 'ul2r'
    print(id_repr(sh.layout))
    # sh._extract_node_paths('ur2d', 'dl2r')
    print(id_repr(sh.nodes))
    print(id_repr(sh.paths[0]))
    # print(sh.adjacency[1])

    print(sh.structure_matrix)
    print(sh.input_matrix)
    print(sh.output_matrix)
    print(sh.phi_matrix)
    print(sh.temperature_matrix[1] - 273.15)
    print(sh.temperature_outputs[1] - 273.15)

    # print(sh)
    print(sh.heat_flows)
    sh._adjust_temperatures()
    print(sh.heat_flows)
    print(sh)

    for i in range(5):
        sh._adjust_temperatures()
        print(sh.heat_flows)
        print(sh)
        print(sh.temperature_outputs[1] - 273)
    print(sh)
    print(sh.heat_flows)
