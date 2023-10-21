import matplotlib.offsetbox
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

from .stream import Fluid, Flow
from .exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow


class ExchangerNetwork:
    """
        A class representing a heat exchanger network.

        Args:
            input_flows (list, optional): A list of input flows to the network.
            exchangers (list, optional): A list of heat exchangers in the network.
            output_flows (list, optional): A list of output flows from the network.

        Attributes:
            input_temps (tuple): A tuple containing input temperatures and their dimensionless representation.
            structure_matrix (numpy.ndarray, optional): The structure matrix of the network.
            input_matrix (numpy.ndarray, optional): The input matrix of the network.
            output_matrix (numpy.ndarray, optional): The output matrix of the network.

    """

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
        """
        Get or set the list of input flows to the network.

        Args:
            value (list): A list of input flows.

        Raises:
            NotImplementedError: If the provided value is not a list.

        """
        return self._input_flows

    @input_flows.setter
    def input_flows(self, value):
        if isinstance(value, list):
            self._input_flows = value
        else:
            raise NotImplementedError

    @property
    def exchangers(self):
        """
        Get or set the list of heat exchangers in the network.

        Args:
            value (list or HeatExchanger): A list of heat exchangers or a single heat exchanger.

        Raises:
            NotImplementedError: If the provided value is not a list or a HeatExchanger object.

        """
        return self._exchangers

    @exchangers.setter
    def exchangers(self, value):
        if isinstance(value, list):
            self._exchangers = value
        elif isinstance(value, HeatExchanger):
            self._exchangers.append(value)

    @property
    def cell_numbers(self):
        """
        Get the number of cells (heat exchangers) in the network.

        Returns:
            int: The number of cells.

        """
        value = len(self.exchangers)
        return value

    @property
    def output_flows(self):
        """
        Get or set the list of output flows from the network.

        Args:
            value (list): A list of output flows.

        Raises:
            NotImplementedError: If the provided value is not a list.

        """
        return self._output_flows

    @output_flows.setter
    def output_flows(self, value):
        if isinstance(value, list):
            self._output_flows = value
        else:
            raise NotImplementedError

    @property
    def input_temps(self):
        """
        Get or set the input temperatures and their dimensionless representation.

        Args:
            value (numpy.ndarray): The dimensionless representation

        Returns:
            tuple: A tuple containing input temperatures and their dimensionless representation.

        """
        value = self._input_temps
        if value[0] is None:  # only if input temps is set directly
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
        """
        Get or set the structure matrix of the network.

        Args:
            value (numpy.ndarray): The structure matrix.

        Raises:
            NotImplementedError: If the provided value is not a numpy.ndarray.

        """
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
        """
        Get or set the input matrix of the network.

        Args:
            value (numpy.ndarray): The input matrix.

        Raises:
            NotImplementedError: If the provided value is not a numpy.ndarray.

        """
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
        """
        Get or set the output matrix of the network.

        Args:
            value (numpy.ndarray): The output matrix.

        Raises:
            NotImplementedError: If the provided value is not a numpy.ndarray.

        """
        try:
            return self._output_matrix
        except AttributeError:
            pass

    @output_matrix.setter
    def output_matrix(self, value):
        """
        Get the temperature input matrix.

        Returns:
            numpy.ndarray: The temperature input matrix.

        """
        if isinstance(value, np.ndarray):
            self._output_matrix = value
        else:
            raise NotImplementedError

    @property
    def temperature_input_matrix(self):
        return self.input_temps[1]

    @property
    def phi_matrix(self):
        """
        Get or set the phi matrix of the network.

        Args:
            value (numpy.ndarray): The phi matrix.

        Raises:
            NotImplementedError: If the provided value is not a numpy.ndarray.

        """
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

    def _cells_characteristic(self):
        """
        Calculate the characteristics of the network cells.

        Returns:
            numpy.ndarray: The calculated characteristics of the network cells.

        """
        phi = self.phi_matrix
        s = self.structure_matrix
        inp = self.input_matrix

        ps = phi @ s
        identity = np.eye(ps.shape[0])

        value = inv((identity - ps)) @ phi @ inp
        return value

    @property
    def temperature_matrix(self):
        """
        Get the temperature matrix of the network.

        Returns:
            tuple: A tuple containing the temperature matrix and its dimensional representation.

        """
        value = self._cells_characteristic() @ self.temperature_input_matrix
        return value, self._dimles_2_temp(value)

    @property
    def network_characteristics(self):
        """
        Get the network characteristics.

        Returns:
            numpy.ndarray: The network characteristics.

        """
        return self.output_matrix @ self._cells_characteristic()

    def _dimles_2_temp(self, matrix):
        """
        converts the dimensionless temperatures back to temperature in K
        based on the maximal and minimal input temperatures.
        """
        temps = self.input_temps[0]
        min_temp = min(temps)
        max_temp = max(temps)
        return (max_temp - min_temp) * matrix + min_temp

    @property
    def temperature_outputs(self):
        """
        Get the temperature outputs of the network.

        Returns:
            tuple: A tuple containing the temperature outputs and their dimensional representation.

        """
        value = self.output_matrix @ self.temperature_matrix[0]
        return value, self._dimles_2_temp(value)

    def temperature_outputs_str(self):
        """
        Return a formatted string for the temperature outputs of the network.

        Returns:
            str: A string containing the temperature outputs of the network.

        """
        pass

    @property
    def heat_flows(self):
        pass

    def heat_flows_str(self):
        """
        Return a formatted string for the heat flows of the network.

        Returns:
            str: A string containing the heat flows of the network.

        """
        try:
            return f"\theat flows q_1=%.2f kW,\tq_2=%.2f kW\n" % (self.heat_flows[0] * 1e-3, self.heat_flows[1] * 1e-3)
        except TypeError:
            return ""

    def _vis_temperature_adjusment_development(self, temp_list, ax=None, **ax_parameters):
        """
        Visualize temperature adjustment development or iterations.

        Args:
            temp_list (list): A list of temperature data to visualize.
            ax (matplotlib.axes.Axes, optional): The matplotlib axes to use for plotting. If not provided, a new figure is created.
            **ax_parameters: Additional parameters to customize the plot.

        """
        vis_temp_progress(temp_list, 'temperature adjustment development', ax,
                          label_data=[f'network output temperature {i + 1}' for i in range(len(temp_list))],
                          label_x='iterations', **ax_parameters)

    def _vis_flow_temperature_development(self, temp_list, ax=None, **ax_parameters):
        """
        Visualize flow temperature development over the heat exchanger cells.

        Args:
            temp_list (list): A list of temperature data to visualize.
            ax (matplotlib.axes.Axes, optional): The matplotlib axes to use for plotting. If not provided, a new figure is created.
            **ax_parameters: Additional parameters to customize the plot.

        """
        vis_temp_progress(temp_list, 'flow temperature development', ax, label_x='cell passed by flow', **ax_parameters)

    def extended_info(self):
        """
            Return extended information about the network, including information about input flows, output flows, and heat exchangers.

            Returns:
                str: A string containing extended information about the network

        """
        output = self.__repr__()
        for i, ex in enumerate(self.exchangers):
            output += f"\ncell:{i}\n{ex}\n"
        return output

    def __repr__(self):
        output = "Heat Exchanger Network:\n"
        output += f"\tcell numbers: {self.cell_numbers}\n"
        output += self.heat_flows_str()

        if all(isinstance(item, Flow) for item in self.input_flows):
            output += f"input flows: n={len(self.input_flows)}\n"
            for i, flow in enumerate(self.input_flows):
                output += f"\tflow {i}: {flow.mean_fluid.title}, temp= {flow.mean_fluid.temperature - 273.15:.2f}°C\n"

        if all(isinstance(item, Flow) for item in self.output_flows):
            output += f"output flows: n={len(self.output_flows)}\n"
            for i, flow in enumerate(self.output_flows):
                output += f"\tflow {i}: {flow.mean_fluid.title}, temp= {flow.mean_fluid.temperature - 273.15:.2f}°C\n"
        return output


def vis_temp_progress(data_list, title: str = 'temperature development', ax=None, **ax_parameters):
    """
       Visualize temperature progression.

       Args:
           data_list (list): A list of temperature data to visualize.
           title (str, optional): The title of the plot. Default is 'temperature development'.
           ax (matplotlib.axes.Axes, optional): The matplotlib axes to use for plotting. If not provided, a new figure is created.
           **ax_parameters: Additional parameters to customize the plot.
               label_data (list, optional): A list of labels for the temperature data series. Default is ['temperature 1', 'temperature 2', ...].
               label_x (str, optional): Label for the x-axis. Default is 'development'.
               label_y (str, optional): Label for the y-axis. Default is 'temperatures'.
               min_y (float, optional): Minimum value for the y-axis.
               max_y (float, optional): Maximum value for the y-axis.

       """
    if ax is None:
        fig, ax = plt.subplots()

    data_list = [data - 273.15 for data in data_list]

    label_data = ax_parameters.get('label_data', [f'temperature {i + 1}' for i in range(len(data_list))])
    # for i, data_row in enumerate(zip(*data_list)):
    # ax.plot(data_row, label=f'temperature {i + 1}')
    for i, data in enumerate(zip(*data_list)):
        ax.plot(data, label=label_data[i])

    label_x = ax_parameters.get('label_x', 'development')
    label_y = ax_parameters.get('label_y', 'temperatures')
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)

    min_y = ax_parameters.get('min_y', None)  # Retrieve min_y from ax_parameters or set to None
    max_y = ax_parameters.get('max_y', None)  # Retrieve max_y from ax_parameters or set to None
    if min_y is not None and max_y is not None:
        ax.set_ylim(min_y, max_y)

    x_ticks = np.arange(0, len(data_list), 1)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(int(x)) for x in x_ticks])

    ax.set_title(title)
    ax.grid(True)
    ax.legend()


def vis_setups(network_list: list, plot_function, fig_title: str = "", **ax_parameters):
    """
    Visualize multiple network setups.

    Args:
        network_list (list): A list of ExchangerNetwork objects to visualize.
        plot_function (callable): A function for plotting each network setup.
        fig_title (str, optional): The title of the figure. Default is an empty string.
        **ax_parameters: Additional parameters to customize the plot.

    """
    num_networks = len(network_list)

    num_cols = 6
    num_rows = (num_networks + num_cols - 1) // num_cols

    fig, axs = plt.subplots(num_rows, num_cols, sharex='row', sharey='col', figsize=(3 * num_cols, 3 * num_rows))

    fig.suptitle(fig_title, fontsize=25)

    for i, (network, ax) in enumerate(zip(network_list, axs.ravel())):
        plot = getattr(network, plot_function)
        plot(ax, **ax_parameters)
        ax.set_title(f"setup: {i + 1}")
    for ax in axs.ravel()[num_networks:]:
        ax.set_visible(False)

    plt.tight_layout()
    # plt.subplots_adjust(hspace=0.5,wspace=2)
