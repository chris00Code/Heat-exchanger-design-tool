import matplotlib.offsetbox
import numpy as np

from numpy.linalg import inv
import matplotlib.pyplot as plt
from stream import Fluid, Flow
from exchanger import HeatExchanger, ParallelFlow, CounterCurrentFlow
from network_setups import *


class ExchangerNetwork:
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
        return self._input_flows

    @input_flows.setter
    def input_flows(self, value):
        if isinstance(value, list):
            self._input_flows = value
        else:
            raise NotImplementedError

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
    def cell_numbers(self):
        value = len(self.exchangers)
        return value

    @property
    def output_flows(self):
        return self._output_flows

    @output_flows.setter
    def output_flows(self, value):
        if isinstance(value, list):
            self._output_flows = value
        else:
            raise NotImplementedError

    @property
    def input_temps(self):
        value = self._input_temps
        if value[0] is None:  # only if input temps is set dirrectly
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
        try:
            return self._output_matrix
        except AttributeError:
            pass

    @output_matrix.setter
    def output_matrix(self, value):
        if isinstance(value, np.ndarray):
            self._output_matrix = value
        else:
            raise NotImplementedError

    @property
    def temperature_input_matrix(self):
        return self.input_temps[1]

    @property
    def phi_matrix(self):
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
        phi = self.phi_matrix
        s = self.structure_matrix
        inp = self.input_matrix

        ps = phi @ s
        identity = np.eye(ps.shape[0])

        value = inv((identity - ps)) @ phi @ inp
        return value

    @property
    def temperature_matrix(self):
        value = self._cells_characteristic() @ self.temperature_input_matrix
        return value, self._dimles_2_temp(value)

    @property
    def network_characteristics(self):
        return self.output_matrix @ self._cells_characteristic()

    def _dimles_2_temp(self, matrix):
        temps = self.input_temps[0]
        min_temp = min(temps)
        max_temp = max(temps)
        return (max_temp - min_temp) * matrix + min_temp

    @property
    def temperature_outputs(self):
        value = self.output_matrix @ self.temperature_matrix[0]
        return value, self._dimles_2_temp(value)

    def temperature_outputs_str(self):
        pass

    @property
    def heat_flows(self):
        pass

    def heat_flows_str(self):
        try:
            return f"\theat flows q_1=%.2f kW,\tq_2=%.2f kW\n" % (self.heat_flows[0] * 1e-3, self.heat_flows[1] * 1e-3)
        except TypeError:
            return ""

    def _vis_temperature_adjusment_development(self, temp_list):
        vis_temp_progress(temp_list, 'temperature adjustment development')

    def _vis_flow_temperature_development(self, temp_list):
        vis_temp_progress(temp_list, 'flow temperature development')

    def extended_info(self):
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


def vis_temp_progress(data_list, title: str = 'temperature development'):
    fig, ax = plt.subplots()

    data_list = [data - 273.15 for data in data_list]

    for i, data_row in enumerate(zip(*data_list)):
        ax.plot(data_row, label=f'temperature {i + 1}')

    ax.set_xlabel('development')
    ax.set_ylabel('temperatures')
    ax.set_title(title)
    ax.grid(True)
    ax.legend()


def vis_setups(network_list: list, plot_function, fig_title: str = "", description: str = None, **ax_parameters):
    """
    num_networks = len(network_list)

    num_rows = (num_networks + 5) // 6
    num_cols = (num_networks + num_rows - 1) // num_rows

    fig, axs = plt.subplots(num_rows, num_cols, sharex='row', sharey='col', figsize=(15, 3 * num_rows))

    fig.suptitle(fig_title, fontsize=25)

    for i, (network, ax) in enumerate(zip(network_list, axs.ravel())):
        plot = getattr(network, plot_function)
        plot(ax, **ax_parameters)
        ax.set_title(f"setup: {i + 1}")
    for ax in axs.ravel()[num_networks:]:
        ax.set_visible(False)

    if description is not None:
        fig.subplots_adjust(top=0.85)  # Leave space for the textbox above the subplots
        anchored_text = matplotlib.offsetbox.AnchoredText(description, loc='upper center', frameon=True)
        fig.add_artist(anchored_text)
    plt.tight_layout()
    """

    from matplotlib.gridspec import GridSpec
    from matplotlib.offsetbox import AnchoredText

    """
    num_networks = len(network_list)

    num_rows = (num_networks + 5) // 6
    num_cols = (num_networks + num_rows - 1) // num_rows

    fig = plt.figure(figsize=(15, 3 * num_rows))
    if description is not None:
        #num_rows += 1  # Add an extra row for the text box
        num_cols+=1
        description = 'description:\n' + description.replace('\t','   ')

    gs = GridSpec(num_rows, num_cols, figure=fig)

    fig.suptitle(fig_title, fontsize=16)  # Set the main title of the figure

    for i, (network, col) in enumerate(zip(network_list, gs)):
        ax = fig.add_subplot(col)
        plot = getattr(network, plot_function)
        plot(ax, **ax_parameters)
        ax.set_title(f"setup: {i + 1}")

    if description is not None:
        anchored_text = AnchoredText(description, loc='upper left', frameon=False)
        #text_box = fig.add_subplot(gs[-1, :])  # Add subplot for the text box
        text_box = fig.add_subplot(gs[:,-1])
        text_box.add_artist(anchored_text)
        text_box.axis('off')  # Turn off axes for the text box

    plt.tight_layout()
    """
    num_networks = len(network_list)

    n_subplots_col = 6

    num_rows = (num_networks + n_subplots_col - 1) // n_subplots_col
    num_cols = n_subplots_col

    fig = plt.figure(figsize=(15, 5 * num_rows * 2))

    gs = GridSpec(num_rows * 2, num_cols, figure=fig)

    fig.suptitle(fig_title, fontsize=16)  # Set the main title of the figure

    for i, (network, col) in enumerate(zip(network_list, gs)):
        row_index = i//n_subplots_col
        col_index = i% n_subplots_col

        ax = fig.add_subplot(gs[row_index*2, col_index])  # Adjusted for row and col
        plot = getattr(network, plot_function)
        plot(ax, **ax_parameters)
        ax.set_title(f"setup: {i + 1}")

        description = network.flow_orders_str() + network.heat_flows_str() + network.temperature_outputs_str()
        anchored_text = AnchoredText(description.replace('\t','   '), loc='upper center', frameon=False)

        text_box = fig.add_subplot(gs[row_index*2 + 1, col_index])  # Adjusted for row and col
        text_box.add_artist(anchored_text)
        text_box.axis('off')  # Turn off axes for the text box

        """
        if description is not None:
            description = f'setup {i + 1}:\n' + description.replace('\t', '   ')
            anchored_text = AnchoredText(description, loc='upper left', frameon=False)
            ax.add_artist(anchored_text)
        """
    #plt.tight_layout()