import math

from exchanger_types import *
from itertools import permutations
from matrix_converter import heat_flow_repr
"""
input_locations = ['ul2r', 'dl2r', 'ur2l', 'dr2l', 'ul2d', 'ur2d', 'dl2u', 'dr2u']


def test_input_arrangements():
    result = list(permutations(input_locations, 2))
    # result = [(a, b) for a, b in result if a != b]
    return result


def vis_results(networks):
    num_subplots = len(networks)

    fig, axs = plt.subplots(1, num_subplots, figsize=(15, 5))

    for i, (network, ax) in enumerate(zip(networks, axs)):
        network.vis_heat_flow(ax)
        description = f'Description for Object {network.flow_order_1}\n' + network.heat_flows_str()
        ax.text(0.5, 1.1, description, transform=ax.transAxes, ha='center')
    plt.tight_layout()
    plt.show()
"""

"""def plot_networks(network_list):
    num_networks = len(network_list)

    num_rows = (num_networks + 5) // 6

    fig, axs = plt.subplots(num_rows, 6, sharex='row', sharey='col', figsize=(15, 3 * num_rows))

    vmax = max([heat_flow_repr(netw.layout_matrix).max() for netw in network_list])

    for i, (network, ax) in enumerate(zip(network_list, axs.ravel())):
        network.vis_heat_flow(ax, 0, vmax)
        description = f'flow order: 1={network.flow_order_1},2={network.flow_order_2}\n' \
                      + network.heat_flows_str() \
                      + network.temperature_outputs_str()
        ax.annotate(description, xy=(0.5, 1.20), fontsize=6, xycoords='axes fraction', ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'))
        ax.set_title("")

    plt.subplots_adjust(wspace=0.5, hspace=1.5)

    # plt.show()


def vis_setups_heatflow(network_list: list):
    num_networks = len(network_list)

    num_rows = (num_networks + 5) // 6

    fig, axs = plt.subplots(num_rows, 6, sharex='row', sharey='col', figsize=(15, 3 * num_rows))

    vmax = max([heat_flow_repr(netw.layout_matrix).max() for netw in network_list])

    for i, (network, ax) in enumerate(zip(network_list, axs.ravel())):
        network.vis_heat_flow(ax, 0, vmax)
        description = f'flow order: 1={network.flow_order_1},2={network.flow_order_2}\n' \
                      + network.heat_flows_str() \
                      + network.temperature_outputs_str()
        ax.annotate(description, xy=(0.5, 1.20), fontsize=6, xycoords='axes fraction', ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'))
        ax.set_title("")

    plt.subplots_adjust(wspace=0.5, hspace=1.5)


def vis_setups_temp_progress(network_list: list):
    num_networks = len(network_list)

    num_rows = (num_networks + 5) // 6

    fig, axs = plt.subplots(num_rows, 6, sharex='row', sharey='col', figsize=(15, 3 * num_rows))

    vmax = max([heat_flow_repr(netw.layout_matrix).max() for netw in network_list])

    for i, (network, ax) in enumerate(zip(network_list, axs.ravel())):
        network.vis_flow_temperature_development(ax, 0, vmax)
        description = f'flow order: 1={network.flow_order_1},2={network.flow_order_2}\n' \
                      + network.heat_flows_str() \
                      + network.temperature_outputs_str()
        ax.annotate(description, xy=(0.5, 1.20), fontsize=6, xycoords='axes fraction', ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'))
        ax.set_title("")

    plt.subplots_adjust(wspace=0.5, hspace=1.5)
"""
