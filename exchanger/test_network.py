import unittest

import numpy as np

from network import ExchangerNetwork
from exchanger import ParallelFlow, CounterCurrentFlow
from stream import Fluid, Flow


class NetworkTests(unittest.TestCase):
    flow_1 = Flow(Fluid("Water", temperature = 273.15 + 15), 1)
    flow_2 = Flow(Fluid("Air",temperature = 273.15), 5)
    exchanger_1 = ParallelFlow(flow_1, flow_2, 10)
    exchanger_2 = CounterCurrentFlow(flow_1, flow_2, 50)

    def test_init_empty(self):
        network = ExchangerNetwork()
        self.assertEqual(network.input_flows, [])
        self.assertEqual(network.exchangers, [])
        self.assertEqual(network.output_flows, [])

    def test_init(self):
        flows = [self.flow_1, self.flow_2]
        network = ExchangerNetwork(flows)
        self.assertEqual(network.input_flows, flows)
        self.assertEqual(network.exchangers, [])
        self.assertEqual(network.output_flows, [])

    def test_exchanger_setter(self):
        network = ExchangerNetwork()
        network.exchangers = self.exchanger_1
        self.assertEqual(network.exchangers[0], self.exchanger_1)

        network.exchangers = self.exchanger_2
        self.assertEqual(network.exchangers[0], self.exchanger_1)
        self.assertEqual(network.exchangers[1], self.exchanger_2)

        network = ExchangerNetwork()
        exchangers = [self.exchanger_2, self.exchanger_1]
        network.exchangers = exchangers
        self.assertEqual(network.exchangers[0], self.exchanger_2)
        self.assertEqual(network.exchangers[1], self.exchanger_1)

    def test_input_temps(self):
        network = ExchangerNetwork()
        self.assertIsInstance(network.input_temps, tuple)
        self.assertEqual(network.input_temps[0], [])
        flows = [self.flow_1, self.flow_2]
        network = ExchangerNetwork(flows)

        network.input_flows.append( Flow(Fluid("Water", temperature = 273.15 + 50), 1))
        self.assertEqual(network.input_temps[1][0], 0)
        self.assertEqual(network.input_temps[1][1], 0)
        self.assertEqual(network.input_temps[1][2], 1)






if __name__ == '__main__':
    unittest.main()
