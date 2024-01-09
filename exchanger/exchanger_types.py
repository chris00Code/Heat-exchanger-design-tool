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
    """
        A class representing a two-flow heat exchanger network.

        Attributes:
            flow_orders (list): A list of valid flow orders for the two flows.
            auto_adjust (bool): A flag indicating whether to automatically adjust temperatures and fluid properties.
            layout_matrix (np.ndarray): The layout matrix representing the arrangement of heat exchangers.
            in_flow_1 (Flow): The input flow for the first flow path.
            in_flow_2 (Flow): The input flow for the second flow path.
            flow_order_1 (str): The flow order for the first flow path.
            flow_order_2 (str): The flow order for the second flow path.


        Args:
            layout_matrix (np.ndarray): The layout matrix representing the arrangement of heat exchangers.
            flow_1 (Flow): The input flow for the first flow path.
            flow_order_1 (str): The flow order for the first flow path.
            flow_2 (Flow): The input flow for the second flow path.
            flow_order_2 (str): The flow order for the second flow path.

       """
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
        """
        Get or set the layout matrix representing the arrangement of heat exchangers.

        Setter enforces the matrix to be a numpy array or None.

        Args:
            value (np.ndarray or None): A matrix representing the layout of the heat exchanger.

        Raises:
            NotImplementedError: If the input is not a numpy array or None.
        """
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
        """
        Get or set the list of exchangers in the network.

        Args:
            value (list or HeatExchanger): A list of heat exchangers or a single heat exchanger.

        Raises:
            NotImplementedError: If the provided value is not a list or a HeatExchanger object.
        """
        return self._exchangers_flattened[0]

    @exchangers.setter
    def exchangers(self, value):
        if not value:
            self._exchangers_flattened = NotImplemented, NotImplemented
        else:
            raise NotImplementedError

    @property
    def in_flow_1(self):
        """
        Get or set the input flow for the first flow path.

        Args:
            value (Flow): The new value for the input flow.

        Raises:
            NotImplementedError: If the provided value is not a Flow object.
        """
        return self.input_flows[0]

    @in_flow_1.setter
    def in_flow_1(self, value):
        if isinstance(value, Flow):
            self.input_flows[0] = value
            self._fill()

    @property
    def in_flow_2(self):
        """
        Get or set the input flow for the second flow path.

        Args:
            value (Flow): The new value for the input flow.

        Raises:
            NotImplementedError: If the provided value is not a Flow object.
        """
        return self.input_flows[1]

    @in_flow_2.setter
    def in_flow_2(self, value):
        if isinstance(value, Flow):
            self.input_flows[1] = value
            self._fill()

    @property
    def out_flow_1(self):
        """
        Get or set the output flow for the first flow path.

        Parameters:
            - value (Flow): The new value for the output flow.

        Raises:
            - NotImplementedError: If the provided value is not a Flow object.
        """
        self._flatten()
        return self.output_flows[0]

    @out_flow_1.setter
    def out_flow_1(self, value):
        if isinstance(value, Flow):
            self.output_flows[0] = value

    @property
    def out_flow_2(self):
        """
        Get or set the output flow for the second flow path.

        Parameters:
            - value (Flow): The new value for the output flow.

        Raises:
            - NotImplementedError: If the provided value is not a Flow object.
        """
        return self.output_flows[1]

    @out_flow_2.setter
    def out_flow_2(self, value):
        if isinstance(value, Flow):
            self.output_flows[1] = value

    # # TODO check shape and flow order

    @property
    def flow_order_1(self):
        """
        Get or set the flow order for the first flow path.

        Args:
            value (str): The new value for the flow order.

        Raises:
            NotImplementedError: If the provided value is not in the list of flow orders or None.
        """
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
        """
        Get or set the flow order for the first flow path.

        Args:
            value (str): The new value for the flow order.

        Raises:
            NotImplementedError: If the provided value is not in the list of flow orders or None.
        """
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
        """
        Get a string representation of the flow orders.

        Returns:
            str: A string representation of the flow orders.
        """
        output = f"flow order: flow_1:{self.flow_order_1}\tflow_2:{self.flow_order_2}\n"
        return output

    @property
    def heat_flows(self):
        """
        Get the total heat flows in the network.

        Returns:
            Tuple: A tuple containing the total heat flows for flow path 1 and flow path 2.

        """
        q_1, q_2 = 0, 0
        for ex in self.exchangers:
            q_1 += ex.heat_flows[0]
            q_2 += ex.heat_flows[1]
        return q_1, q_2

    @property
    def cell_numbers(self):
        """
        Get the number of cells in the layout matrix.

        Returns:
            int: The number of cells in the layout matrix.

        """
        layout_matrix = self.layout_matrix
        if layout_matrix is None:
            value = 0
        else:
            value = layout_matrix.size
        return value

    @property
    def total_transferability(self):
        """
        Get the total heat transferability of the exchangers.

        Returns:
            float: The total heat transferability of the exchangers.

        """
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
        """
        Get a list of nodes in the network.

        Returns:
            list: A list containing input flows, exchangers, and output flows.

        """
        value = self.input_flows + self.exchangers + self.output_flows
        return value

    @property
    def paths(self):
        """
        Get the paths of nodes in the network.

        Returns:
            Tuple: A tuple containing the paths for flow path 1 and flow path 2.

        """
        try:
            value = self._paths
        except AttributeError:
            self._extract_node_paths()
            value = self._paths
        return value

    def _fill(self):
        """
        Fill the layout matrix with HeatExchanger objects.

        This private method is responsible for filling the layout matrix with HeatExchanger objects. It is called during
        the initialization process.

        """
        pass

    def _flatten(self):
        """
        Flatten the layout matrix and set in and out fluids for exchangers.

        This private method flattens the layout matrix according to flow orders, sets in and out fluids for exchangers,
        and sets the output flows.

        """
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
        Set in and out fluids for exchangers based on flow order.

        This private method sets the in and out fluids for exchangers according to the specified flow order.

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
        """
        Extract node paths for flow paths 1 and 2.

        This private method extracts node paths for flow paths 1 and 2 and sets them to the _paths attribute.

        """
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
        """
        Get the adjacency matrices for flow paths 1 and 2.

        Returns:
            Tuple: A tuple containing the adjacency matrices for flow paths 1 and 2.

        """
        try:
            value = self._adj_1, self._adj_2
        except AttributeError:
            self._matrix_representation()
            value = self._adj_1, self._adj_2
        return value

    def _matrix_representation(self):
        """
        Generate adjacency matrices for flow paths 1 and 2.

        This private method utilizes the NetworkX library to create directed graphs for flow paths 1 and 2 and generate
        adjacency matrices. The adjacency matrices are then set to the _adj_1 and _adj_2 attributes.

        """
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
        """
        Get the structure matrix of the exchanger network.

        Returns:
            numpy.ndarray: Structure matrix of the exchanger network.

        """
        s11 = self.adjacency[0][2:-2, 2:-2]
        s22 = self.adjacency[1][2:-2, 2:-2]
        zeros = np.zeros_like(s11)
        structure = np.block([[s11, zeros], [zeros, s22]]).T
        return structure

    @property
    def input_matrix(self):
        """
        Get the input matrix of the exchanger network.

        Returns:
            numpy.ndarray: Input matrix of the exchanger network.

        """
        in_1 = self.adjacency[0][:2, 2:-2]
        in_2 = self.adjacency[1][:2, 2:-2]
        input = np.hstack((in_1, in_2)).T
        return input

    @property
    def output_matrix(self):
        """
        Get the output matrix of the exchanger network.

        Returns:
            numpy.ndarray: Output matrix of the exchanger network.

        """
        out_1 = self.adjacency[0][2:-2, -2:]
        out_2 = self.adjacency[1][2:-2, -2:]
        output = np.vstack((out_1, out_2)).T
        return output

    @property
    def phi_matrix(self):
        """
        Get the phi matrix of the exchanger network.

        Returns:
            numpy.ndarray: Phi matrix of the exchanger network.

        """
        _ = self.structure_matrix
        return super().phi_matrix

    def _adjust_temperatures(self, iterations=1):
        """
        Adjust temperatures in the exchanger network and update fluid parameters.

        This method iteratively adjusts temperatures in the exchanger network, which leads to a more accurate calculation
        of fluid parameters. The adjustment is performed based on the specified flow orders.

        Args:
            iterations (int, optional): Number of iterations for temperature adjustment. Defaults to 1.

        """
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
        """
        Get a string representation of temperature outputs in °C.

        Returns:
            str: String representation of temperature outputs in °C.

        """
        try:
            return f"\ttemperature outputs: flow 1=%.2f °C,\tflow 2=%.2f °C\n" % (
                self.temperature_outputs[1][0, 0] - 273.15, self.temperature_outputs[1][1, 0] - 273.15)
        except TypeError:
            return ""

    def vis_heat_flow(self, ax=None, **ax_parameters):
        """
        Visualize the heat flow in the exchanger network.

        Args:
            ax (matplotlib.axes.Axes, optional): Matplotlib axes to plot on. If None, a new figure and axes will be created.
            **ax_parameters: Additional keyword arguments for Matplotlib axes.

        """
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

        start_point,direction_list = get_direction_list(self.layout_matrix,self.flow_order_1)
        add_arrows(ax,direction_list,start_point,text='flow 1')

        start_point,direction_list = get_direction_list(self.layout_matrix,self.flow_order_2)
        add_arrows(ax,direction_list,start_point,text='flow 2',color='blue')


    def vis_temperature_adjustment_development(self):
        """
        Visualize the development of temperature adjustment over iterations.

        """
        super()._vis_temperature_adjusment_development(self._temperature_adjustment_development)

    def vis_flow_temperature_development(self, ax=None, **ax_parameters):
        """
        Visualize the development of flow temperatures in the exchanger network.

        Args:
            ax (matplotlib.axes.Axes, optional): Matplotlib axes to plot on. If None, a new figure and axes will be created.
            **ax_parameters: Additional keyword arguments for Matplotlib axes.

        """
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
        """
        Get all possible input flow order arrangements.

        Returns:
            list: List of tuples representing all possible input flow order arrangements.

        """
        result = list(permutations(ExchangerTwoFlow.flow_orders, 2))
        return result

    def __repr__(self):
        """
        String representation of the ExchangerTwoFlow object.

        If auto_adjust is True, the temperature adjustment is automatically performed before generating the string representation.

        Returns:
            str: String representation of the object.

        """
        if self.auto_adjust:
            try:
                self._adjust_temperatures(5)
            except AttributeError:
                pass
        return super().__repr__()


class ExchangerEqualCells(ExchangerTwoFlow):
    """
    A class representing a two-flow heat exchanger network with cells of equal properties.

    Attributes:
        exchangers_type (str): The type of heat exchangers used in the network.
        assembly (Assembly): The assembly object containing all constructive parameters for the network.
        total_transferability (float): The total heat transferability of the exchangers.
    """
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
        """
        Get or set the type of heat exchangers used in the network.

        Args:
            value (str): The type of heat exchangers.

        Raises:
            NotImplementedError: If the provided value is not in the list of available class names.

        """
        return self._exchangers_type

    @exchangers_type.setter
    def exchangers_type(self, value):
        if value in get_available_class_names(exchanger.exchanger):
            self._exchangers_type = value
        else:
            raise NotImplementedError

    @property
    def shape(self):
        """
        Get or set the shape of the layout matrix.

        Args:
            value (tuple): The shape of the layout matrix.

        Raises:
            NotImplementedError: If the provided value is not a tuple.

        """
        return self.layout_matrix.shape

    @shape.setter
    def shape(self, value):
        self.layout_matrix = value

    @property
    def layout_matrix(self):
        """
        Get or set the layout matrix of the network.

        Args:
            shape (tuple): The shape of the layout matrix.

        Raises:
            NotImplementedError: If the provided value is not a tuple.

        """
        return super().layout_matrix

    @layout_matrix.setter
    def layout_matrix(self, shape):
        if isinstance(shape, tuple):
            self._layout_matrix = np.zeros(shape, dtype=HeatExchanger)
        else:
            raise NotImplementedError

    @property
    def assembly(self):
        """
        Get or set the assembly object containing all constructive parameters for the network.

        Args:
            value (Assembly or NotImplemented): The assembly object.

        Raises:
            NotImplementedError: If the provided value is not an Assembly object or NotImplemented.

        """
        return self._assembly

    @assembly.setter
    def assembly(self, value):
        if isinstance(value, Assembly) or value is NotImplemented:
            self._assembly = value
        else:
            raise NotImplementedError

    @property
    def total_transferability(self):
        """
        Get or set the total heat transferability of the exchangers.

        Args:
            value (float): The total heat transferability.

        Raises:
            NotImplementedError: If the provided value is not a float.

        """
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
         Fill the layout matrix with Heat Exchanger objects of equal type.
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
        """
        Create a new instance of a heat exchanger of the specified class.

        Args:
            ex_class (class): The class of the heat exchanger.

        Returns:
            HeatExchanger: The new instance of the heat exchanger.

        Raises:
            ValueError: If input flows are not implemented yet.

        """
        if not self.input_flows == [NotImplemented, NotImplemented]:
            flow_1, flow_2 = self.input_flows[0].clone(), self.input_flows[1].clone()
            ex = ex_class(flow_1, flow_2)
            self.__set_transferability(ex)
            return ex
        else:
            raise ValueError("Flows not implemented yet")

    def __set_transferability(self, exchanger):
        """
        Set the heat transferability for the given exchanger.

        Args:
            exchanger (HeatExchanger): The heat exchanger to set the transferability for.

        """
        try:
            exchanger.heat_transferability = self.total_transferability / self.cell_numbers
        except TypeError:
            pass
        except ZeroDivisionError:
            pass
