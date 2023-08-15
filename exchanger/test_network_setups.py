import unittest

from network_setups import *
from test_exchanger_types import init_extype


class NetworkSetupTest(unittest.TestCase):

    def test_arrangements(self):
        networks = []
        for inp in test_input_arrangements():
            netw = init_extype()
            netw.flow_order_1 = inp[0]
            netw.flow_order_2 = inp[1]
            netw._adjust_temperatures()
            networks.append(netw)

        #for net in networks:
        #    print(net[1].temperature_outputs[1] - 273.15)
        plot_networks(networks)

if __name__ == '__main__':
    unittest.main()
