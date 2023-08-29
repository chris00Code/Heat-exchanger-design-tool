import matplotlib.pyplot as plt
import numpy as np


def plot_operating_characteristic(r, n, p):
    for i, r_i in enumerate(r):
        plt.plot(n, p[i], label=f'R={r_i}')
    plt.xlabel('NTU')
    plt.ylabel('P')
    plt.title('Betriebscharakteristik')
    plt.legend()
    plt.grid(True)
    plt.show()


def calc_p_from_characteristic_matrix(network_characteristic):
    if network_characteristic.shape != (2, 2):
        raise NotImplementedError
    else:
        p = network_characteristic[0, 1], network_characteristic[1, 0]
        return p


def plot_thermal_effectiveness_chart(ntu_scale='lin'):
    r = np.linspace(0, 5, 6)
    if ntu_scale == 'lin':
        n = np.linspace(0, 10, 100)
    else:
        raise NotImplementedError
    p = None
    for i, r_i in enumerate(r):
        plt.plot(n, p[i], label=f'R={r_i}')
    plt.xlabel('NTU')
    plt.ylabel('P')
    plt.title('Betriebscharakteristik')
    plt.legend()
    plt.grid(True)
    plt.show()