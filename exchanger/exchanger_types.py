import copy

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow, CrossFlowOneRow
from matrix_converter import *
from numpy.linalg import inv

from network import ExchangerNetwork
from parts import Assembly


class ExchangerTwoFlow(ExchangerNetwork):
    flow_orders = ['ul2r', 'dl2r', 'ur2l', 'dr2l', 'ul2d', 'ur2d', 'dl2u', 'dr2u']

    def __init__(self, layout_matrix: np.ndarray = None, flow_1: Flow = None, flow_order_1: str = None,
                 flow_2: Flow = None, flow_order_2: str = None, ):

        self.layout_matrix = layout_matrix

        if flow_1 is not None and flow_2 is not None:
            input_flows = [flow_1, flow_2]
            out_flow_1 = flow_1.clone()
            out_flow_1.out_fluid = out_flow_1.in_fluid

            out_flow_2 = flow_2.clone()
            out_flow_2.out_fluid = out_flow_2.in_fluid
            output_flows = [out_flow_1, out_flow_2]
            super().__init__(input_flows=input_flows, output_flows=output_flows)
        else:
            super().__init__()

        self.flow_order_1 = flow_order_1
        self.flow_order_2 = flow_order_2

    @property
    def layout_matrix(self):
        return self._layout_matrix

    @layout_matrix.setter
    def layout_matrix(self, value):
        if isinstance(value, np.ndarray) or value is None:
            self._layout_matrix = value
        else:
            raise NotImplementedError

    @property
    def flow_order_1(self):
        return self._flow_order_1

    @flow_order_1.setter
    def flow_order_1(self, value: str):
        if value in self.flow_orders or value is None:
            self._flow_order_1 = value
        else:
            raise NotImplementedError

    @property
    def flow_order_2(self):
        return self._flow_order_2

    @flow_order_2.setter
    def flow_order_2(self, value: str):
        if value in self.flow_orders or value is None:
            self._flow_order_2 = value
        else:
            raise NotImplementedError

    @property
    def cell_numbers(self):
        layout_matrix = self.layout_matrix
        if layout_matrix is None:
            value = 0
        else:
            value = layout_matrix.size
        return value

    @property
    def total_transferability(self):
        values = []
        for ex in self.exchangers:
            values.append(ex.heat_transferability)
        if len(values) == 0:
            value = None
        else:
            value = sum(values)
        return value


class ExchangerEqualCells(ExchangerTwoFlow):
    def __init__(self, shape: tuple = (0, 0),
                 exchangers_type: str = 'CounterCurrentFlow',
                 flow_1: Flow = None, flow_order_1: str = None,
                 flow_2: Flow = None, flow_order_2: str = None,
                 assembly: Assembly = None, total_transferability: float = None):
        # layout matrix can be passed to super constructor because self layout_matrix setter will be used
        self.exchangers_type = exchangers_type

        super().__init__(layout_matrix=shape,
                         flow_1=flow_1, flow_order_1=flow_order_1,
                         flow_2=flow_2, flow_order_2=flow_order_2)

        self.assembly = assembly
        self.total_transferability = total_transferability


    @property
    def exchangers_type(self):
        return self._exchangers_type

    @exchangers_type.setter
    def exchangers_type(self,value):
        self._exchanger_types = value

    @property
    def layout_matrix(self):
        return super().layout_matrix

    @layout_matrix.setter
    def layout_matrix(self, shape):
        if isinstance(shape, tuple):
            self._layout_matrix = np.zeros(shape, dtype=HeatExchanger)
        else:
            raise NotImplementedError

    @property
    def assembly(self):
        return self._assembly

    @assembly.setter
    def assembly(self, value):
        if isinstance(value, Assembly) or value is None:
            self._assembly = value
        else:
            raise NotImplementedError

    @property
    def total_transferability(self):
        value = None
        if self.assembly is not None:
            value = self.assembly.heat_transferability
        if value is None:
            value = self._total_transferability
        else:
            del self._total_transferability
        return value

    @total_transferability.setter
    def total_transferability(self, value):
        if self.assembly is None or self.assembly.heat_transferability is None:
            self._total_transferability = value


class ExchangerEqualCellsTwoFlow(ExchangerNetwork):
    def __init__(self, shape: tuple = (0, 0), type: str = 'CounterCurrentFlow', flow_1: Flow = None,
                 flow_2: Flow = None, assembly: Assembly = None,
                 transferability: float = None):
        self.layout_matrix = shape
        self.type = type

        if flow_1 is not None and flow_2 is not None:
            input_flows = [flow_1, flow_2]
            out_flow_1 = flow_1.clone()
            out_flow_1.out_fluid = out_flow_1.in_fluid

            out_flow_2 = flow_2.clone()
            out_flow_2.out_fluid = out_flow_2.in_fluid
            output_flows = [out_flow_1, out_flow_2]
            super().__init__(input_flows, output_flows=output_flows)
        else:
            super().__init__()

        self.flow_order_1 = 'dl2r'
        self.flow_order_2 = 'ur2d'
        if assembly is None:
            self.transferability = transferability
        else:
            self.assembly = assembly
        try:
            self.fill(self.type)
        except IndexError:
            pass

    @property
    def layout_matrix(self):
        return self._layout_matrix

    @layout_matrix.setter
    def layout_matrix(self, shape):
        if isinstance(shape, tuple):
            self._layout_matrix = np.zeros(shape, dtype=HeatExchanger)
        else:
            raise NotImplementedError

    @property
    def cell_numbers(self):
        return self.layout_matrix.size

    @property
    def total_transferability(self):
        return self._total_transferability

    @total_transferability.setter
    def total_transferability(self, value):
        self._total_transferability = value

    def fill(self, ex_type: str = 'HeatExchanger', order: str = 'equal'):
        """
        fills the Layout with Heat Exchanger objects
        :param ex_type: type of HeatExchanger (must be implemented in exchangers)
        :param order: if equal, all cells are same heat Exchanger type,
                        transferability is divided equal by number of cells
        """
        if order == 'equal':
            ex_class = globals()[ex_type]

            for i in range(self.layout_matrix.shape[0]):
                for j in range(self.layout_matrix.shape[1]):
                    flow_1, flow_2 = self.input_flows[0].clone(), self.input_flows[1].clone()
                    ex = ex_class(flow_1, flow_2)
                    ex.heat_transferability = self.transferability / self.cell_numbers
                    self.layout_matrix[i, j] = ex
        else:
            pass

    @property
    def flow_order_1(self):
        return self._flow_order_1

    @flow_order_1.setter
    def flow_order_1(self, value: str):
        self._flow_order_1 = value

    @property
    def flow_order_2(self):
        return self._flow_order_2

    @flow_order_2.setter
    def flow_order_2(self, value: str):
        self._flow_order_2 = value

    @property
    def nodes(self):
        value = self.input_flows + self.exchangers + self.output_flows
        return value

    @property
    def paths(self):
        try:
            value = self._paths
        except AttributeError:
            self._extract_node_paths()
            value = self._paths
        return value

    def _extract_node_paths(self, order_1: str = None, order_2: str = None):
        if order_1 is not None: self.flow_order_1 = order_1
        if order_2 is not None: self.flow_order_2 = order_2
        in_flow_1, in_flow_2 = self.input_flows[0], self.input_flows[1]
        out_flow_1, out_flow_2 = self.output_flows[0], self.output_flows[1]

        ex_path_1 = flatten(self.layout_matrix, self.flow_order_1)
        self.exchangers = ex_path_1
        path_1 = ex_path_1.copy()
        path_1.insert(0, in_flow_1)
        path_1.append(out_flow_1)

        tuples_list_1 = list_2_tuplelist(path_1)

        ex_path_2 = flatten(self.layout_matrix, self.flow_order_2)
        path_2 = ex_path_2.copy()
        path_2.insert(0, in_flow_2)
        path_2.append(out_flow_2)

        tuples_list_2 = list_2_tuplelist(path_2)

        self.exchangers_flattened = (ex_path_1, ex_path_2)
        self._paths = tuples_list_1, tuples_list_2

    @property
    def heat_flows(self):
        q_1, q_2 = 0, 0
        for ex in self.exchangers:
            q_1 += ex.heat_flows[0]
            q_2 += ex.heat_flows[1]
        return q_1, q_2

    @property
    def adjacency(self):
        try:
            value = self._adj_1, self._adj_2
        except AttributeError:
            self._matrix_representation()
            value = self._adj_1, self._adj_2
        return value

    def _matrix_representation(self):
        path_1, path_2 = self.paths
        nodes = self.nodes
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
    def phi_matrix(self):
        _ = self.structure_matrix
        return super().phi_matrix

    def _adjust_temperatures(self, iterations=1):
        for i in range(iterations):
            out_temp_1, out_temp_2 = self.temperature_outputs[1][0, 0], self.temperature_outputs[1][1, 0]
            self.output_flows[0].in_fluid.temperature = out_temp_1
            self.output_flows[1].in_fluid.temperature = out_temp_2

            cell_out_temps = self.temperature_matrix[1].flatten()
            n = len(cell_out_temps) // 2

            exchangers_flattened_1, exchangers_flattened_2 = self.exchangers_flattened
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

    def temperature_outputs_str(self):
        try:
            return f"\ttemperature outputs: flow 1=%.2f °C,\tflow 2=%.2f °C\n" % (
                self.temperature_outputs[1][0, 0] - 273.15, self.temperature_outputs[1][1, 0] - 273.15)
        except TypeError:
            return ""

    def heat_flow_vis(self, ax=None, vmin=None, vmax=None):
        par_matrix = heat_flow_repr(self.layout_matrix)

        if ax is None:
            fig, ax = plt.subplots()
        if vmin is None:
            vmin = 0
        if vmax is None:
            vmax = par_matrix.max()
        im = ax.imshow(par_matrix, cmap='viridis', interpolation='nearest', vmin=vmin, vmax=vmax)
        ax.set_title('heat flows')
        num_rows, num_cols = par_matrix.shape
        ax.set_xticks(range(num_cols))
        ax.set_xticklabels(range(1, num_cols + 1))
        ax.set_yticks(range(num_rows))
        ax.set_yticklabels(range(1, num_rows + 1))
        plt.colorbar(im, ax=ax, label='heat flow in W')
