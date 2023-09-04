import collections
import copy
import exchanger
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from numpy.linalg import inv
from itertools import permutations

from .stream import Fluid, Flow
from .exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow, CrossFlowOneRow
from .matrix_converter import *
from .utils import get_available_class_names, get_def_or_calc_value
from .network import ExchangerNetwork
from .parts import Assembly


class ExchangerTwoFlow(ExchangerNetwork):
    flow_orders = ['ul2r', 'dl2r', 'ur2l', 'dr2l', 'ul2d', 'ur2d', 'dl2u', 'dr2u']
    auto_adjust = True

    def __init__(self, layout_matrix: np.ndarray = None, flow_1: Flow = None, flow_order_1: str = None,
                 flow_2: Flow = None, flow_order_2: str = None, ):

        self.layout_matrix = layout_matrix
        super().__init__(input_flows=[NotImplemented, NotImplemented], output_flows=[NotImplemented, NotImplemented])
        self.in_flow_1 = flow_1
        self.in_flow_2 = flow_2
        self.flow_order_1 = flow_order_1
        self.flow_order_2 = flow_order_2
        self._fill()
        self._flatten()

    @property
    def layout_matrix(self):
        return self._layout_matrix

    @layout_matrix.setter
    def layout_matrix(self, value):
        if isinstance(value, np.ndarray) or value is None:
            self._layout_matrix = value
            self._flatten()
        else:
            raise NotImplementedError

    @property
    def exchangers(self):
        return self._exchangers_flattened[0]

    @exchangers.setter
    def exchangers(self, value):
        if not value:
            self._exchangers_flattened = NotImplemented, NotImplemented
        else:
            raise NotImplementedError

    @property
    def in_flow_1(self):
        return self.input_flows[0]

    @in_flow_1.setter
    def in_flow_1(self, value):
        if isinstance(value, Flow):
            self.input_flows[0] = value
            self._fill()

    @property
    def in_flow_2(self):
        return self.input_flows[1]

    @in_flow_2.setter
    def in_flow_2(self, value):
        if isinstance(value, Flow):
            self.input_flows[1] = value
            self._fill()

    @property
    def out_flow_1(self):
        self._flatten()
        return self.output_flows[0]

    @out_flow_1.setter
    def out_flow_1(self, value):
        if isinstance(value, Flow):
            self.output_flows[0] = value

    @property
    def out_flow_2(self):
        return self.output_flows[1]

    @out_flow_2.setter
    def out_flow_2(self, value):
        if isinstance(value, Flow):
            self.output_flows[1] = value

    # # TODO check shape and flow order

    @property
    def flow_order_1(self):
        return self._flow_order_1

    @flow_order_1.setter
    def flow_order_1(self, value: str):
        if value in self.flow_orders or value is None:
            try:
                if value is not None and self._flow_order_1 != value:
                    self._fill()
                    self._flow_order_1 = value
                    self._flatten()
                else:
                    raise AttributeError
            except AttributeError:
                self._flow_order_1 = value
        else:
            raise NotImplementedError

    @property
    def flow_order_2(self):
        return self._flow_order_2

    @flow_order_2.setter
    def flow_order_2(self, value: str):
        if value in self.flow_orders or value is None:
            try:
                if value is not None and self._flow_order_2 != value:
                    self._fill()
                    self._flow_order_2 = value
                    self._flatten()
                else:
                    raise AttributeError
            except AttributeError:
                self._flow_order_2 = value
        else:
            raise NotImplementedError

    def flow_orders_str(self):
        output = f"flow order: flow_1:{self.flow_order_1}\tflow_2:{self.flow_order_2}\n"
        return output

    @property
    def heat_flows(self):
        q_1, q_2 = 0, 0
        for ex in self.exchangers:
            q_1 += ex.heat_flows[0]
            q_2 += ex.heat_flows[1]
        return q_1, q_2

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

    def _fill(self):
        pass

    def _flatten(self):
        try:
            flattened_1 = flatten(self.layout_matrix, self.flow_order_1)
            flattened_2 = flatten(self.layout_matrix, self.flow_order_2)
            self._exchangers_flattened = flattened_1, flattened_2

            # set flows
            self._set_in_out_fluids_in_exchangers()

            # set out flows
            out_flow_1 = self._exchangers_flattened[0][-1].flow_1
            self.output_flows[0] = out_flow_1.clone_by_fluid('out')
            out_flow_2 = self._exchangers_flattened[1][-1].flow_2
            self.output_flows[1] = out_flow_2.clone_by_fluid('out')
        except NotImplementedError:
            # if Flows not implemented yet
            pass
        except AttributeError:
            # if layout matrix not implemented yet
            pass

    def _set_in_out_fluids_in_exchangers(self):
        """
        setting in and out fluids according flow order
        :return:
        """
        for i, ex in enumerate(self._exchangers_flattened[0]):
            if i > 0:
                ex.flow_1.in_fluid = prev_out_fluid
            prev_out_fluid = ex.flow_1.out_fluid
        for i, ex in enumerate(self._exchangers_flattened[1]):
            if i > 0:
                ex.flow_2.in_fluid = prev_out_fluid
            prev_out_fluid = ex.flow_2.out_fluid

    def _extract_node_paths(self):
        self._flatten()

        path_1 = self._exchangers_flattened[0].copy()
        path_1.insert(0, self.in_flow_1)
        path_1.append(self.out_flow_1)
        tuples_list_1 = list_2_tuplelist(path_1)

        path_2 = self._exchangers_flattened[1].copy()
        path_2.insert(0, self.in_flow_2)
        path_2.append(self.out_flow_2)
        tuples_list_2 = list_2_tuplelist(path_2)

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
            temperature_outputs = self.temperature_outputs[1]
            try:
                self._temperature_adjustment_development.append(temperature_outputs)
            except AttributeError:
                self._temperature_adjustment_development = [temperature_outputs]

            out_temp_1, out_temp_2 = temperature_outputs[0, 0], temperature_outputs[1, 0]
            self.output_flows[0].in_fluid.temperature = out_temp_1
            self.output_flows[1].in_fluid.temperature = out_temp_2

            cell_out_temps = self.temperature_matrix[1].flatten()
            n = len(cell_out_temps) // 2

            exchangers_flattened_1, exchangers_flattened_2 = self._exchangers_flattened
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

    def vis_heat_flow(self, ax=None, **ax_parameters):
        par_matrix = heat_flow_repr(self.layout_matrix)

        vmin = ax_parameters.pop('vmin', 0)
        vmax = ax_parameters.pop('vmax', par_matrix.max())

        if ax is None:
            fig, ax = plt.subplots()

        im = ax.imshow(par_matrix, cmap='viridis', interpolation='nearest', vmin=vmin, vmax=vmax, **ax_parameters)
        ax.set_title('heat flows')
        num_rows, num_cols = par_matrix.shape
        ax.set_xticks(range(num_cols))
        ax.set_xticklabels(range(1, num_cols + 1))
        ax.set_yticks(range(num_rows))
        ax.set_yticklabels(range(1, num_rows + 1))
        plt.colorbar(im, ax=ax, label='heat flow in W')

    def vis_temperature_adjustment_development(self):
        super()._vis_temperature_adjusment_development(self._temperature_adjustment_development)

    def vis_flow_temperature_development(self, ax=None, **ax_parameters):
        temp_1, temp_2 = [], []
        for ex in self._exchangers_flattened[0]:
            temp_1.append(ex.flow_1.in_fluid.temperature)
        for ex in self._exchangers_flattened[1]:
            temp_2.append(ex.flow_2.in_fluid.temperature)
        temp_1.append(self.out_flow_1.mean_fluid.temperature)
        temp_2.append(self.out_flow_2.mean_fluid.temperature)

        temp_list = [np.array([x, y]) for x, y in zip(temp_1, temp_2)]
        super()._vis_flow_temperature_development(temp_list, ax, **ax_parameters)

    @staticmethod
    def input_arrangements():
        result = list(permutations(ExchangerTwoFlow.flow_orders, 2))
        return result

    def __repr__(self):
        if self.auto_adjust:
            try:
                self._adjust_temperatures(5)
            except AttributeError:
                pass
        return super().__repr__()


class ExchangerEqualCells(ExchangerTwoFlow):
    def __init__(self, shape: tuple = (0, 0),
                 exchangers_type: str = 'HeatExchanger',
                 flow_1: Flow = None, flow_order_1: str = None,
                 flow_2: Flow = None, flow_order_2: str = None,
                 assembly: Assembly = NotImplemented, total_transferability: float = NotImplemented):
        # layout matrix can be passed to super constructor because self layout_matrix setter will be used
        self.exchangers_type = exchangers_type
        self.assembly = assembly
        self.total_transferability = total_transferability
        super().__init__(layout_matrix=shape,
                         flow_1=flow_1, flow_order_1=flow_order_1,
                         flow_2=flow_2, flow_order_2=flow_order_2)

    @property
    def exchangers_type(self):
        return self._exchangers_type

    @exchangers_type.setter
    def exchangers_type(self, value):
        if value in get_available_class_names(exchanger.exchanger):
            self._exchangers_type = value
        else:
            raise NotImplementedError

    @property
    def shape(self):
        return self.layout_matrix.shape

    @shape.setter
    def shape(self, value):
        self.layout_matrix = value

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
        if isinstance(value, Assembly) or value is NotImplemented:
            self._assembly = value
        else:
            raise NotImplementedError

    @property
    def total_transferability(self):
        def_value = self._total_transferability
        if self.assembly is NotImplemented:
            calc_value = NotImplemented
        else:
            calc_value = self.assembly.heat_transferability
        return get_def_or_calc_value(def_value, calc_value)

    @total_transferability.setter
    def total_transferability(self, value):
        self._total_transferability = value
        self._fill()

    def _fill(self):
        """
        fills the Layout with Heat Exchanger objects
        """
        try:
            ex_class = globals()[self.exchangers_type]

            for i in range(self.layout_matrix.shape[0]):
                for j in range(self.layout_matrix.shape[1]):
                    ex = self.__new_ex(ex_class)
                    self.layout_matrix[i, j] = ex
        except AttributeError:
            pass
        except ValueError:
            pass

    def __new_ex(self, ex_class):
        if not self.input_flows == [NotImplemented, NotImplemented]:
            flow_1, flow_2 = self.input_flows[0].clone(), self.input_flows[1].clone()
            ex = ex_class(flow_1, flow_2)
            self.__set_transferability(ex)
            return ex
        else:
            raise ValueError("Flows not implemented yet")

    def __set_transferability(self, exchanger):
        try:
            exchanger.heat_transferability = self.total_transferability / self.cell_numbers
        except TypeError:
            pass
        except ZeroDivisionError:
            pass
