import unittest

import numpy as np

from exchanger.network import ExchangerNetwork
from exchanger.exchanger import ParallelFlow, CounterCurrentFlow
from exchanger.stream import Fluid, Flow


def init_flows():
    flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 1)
    flow_2 = Flow(Fluid("Air", temperature=273.15), 5)
    return flow_1, flow_2


def init_ex():
    flow_1, flow_2 = init_flows()
    exchanger_1 = ParallelFlow(flow_1, flow_2)
    exchanger_2 = CounterCurrentFlow(flow_1, flow_2)
    return exchanger_1, exchanger_2


class NetworkTests(unittest.TestCase):

    def test_init_empty(self):
        network = ExchangerNetwork()
        self.assertEqual(network.input_flows, [])
        self.assertEqual(network.exchangers, [])
        self.assertEqual(network.output_flows, [])

    def test_init(self):
        flow_1, flow_2 = init_flows()
        flows = [flow_1, flow_2]
        network = ExchangerNetwork(flows)
        self.assertEqual(network.input_flows, flows)
        self.assertEqual(network.exchangers, [])
        self.assertEqual(network.output_flows, [])

    def test_exchanger_setter(self):
        ex_1, ex_2 = init_ex()
        network = ExchangerNetwork()
        network.exchangers = ex_1
        self.assertEqual(network.exchangers[0], ex_1)

        network.exchangers = ex_2
        self.assertEqual(network.exchangers[0], ex_1)
        self.assertEqual(network.exchangers[1], ex_2)

        network = ExchangerNetwork()
        exchangers = [ex_2, ex_1]
        network.exchangers = exchangers
        self.assertEqual(network.exchangers[0], ex_2)
        self.assertEqual(network.exchangers[1], ex_1)

    def test_input_temps(self):
        flow_1, flow_2 = init_flows()
        network = ExchangerNetwork()
        self.assertIsInstance(network.input_temps, tuple)
        self.assertEqual(network.input_temps[0], [])
        flows = [flow_1, flow_2]
        network = ExchangerNetwork(flows)

        network.input_flows.append(Flow(Fluid("Water", temperature=273.15 + 50), 1))
        np.testing.assert_equal(network.input_temps[1], np.array([[0.3], [0], [1]]))

    def test_phi_setter(self):
        network = ExchangerNetwork()
        phi = np.array([[0.75, 0., 0., 0., 0.25, 0., 0., 0.],
                        [0., 0.75, 0., 0., 0., 0.25, 0., 0.],
                        [0., 0., 0.75, 0., 0., 0., 0.25, 0.],
                        [0., 0., 0., 0.75, 0., 0., 0., 0.25],
                        [0.25, 0., 0., 0., 0.75, 0., 0., 0.],
                        [0., 0.25, 0., 0., 0., 0.75, 0., 0.],
                        [0., 0., 0.25, 0., 0., 0., 0.75, 0.],
                        [0., 0., 0., 0.25, 0., 0., 0., 0.75]])
        network.phi_matrix = phi
        np.testing.assert_array_equal(network.phi_matrix, phi)

    def test_temperature_output_matrix(self):
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 100), 1)
        flow_2 = Flow(Fluid("Water", temperature=273.15 + 20), 1)
        flows = [flow_1, flow_2]
        network = ExchangerNetwork(flows)
        network.phi_matrix = np.array([[0.75, 0., 0., 0., 0.25, 0., 0., 0.],
                                       [0., 0.75, 0., 0., 0., 0.25, 0., 0.],
                                       [0., 0., 0.75, 0., 0., 0., 0.25, 0.],
                                       [0., 0., 0., 0.75, 0., 0., 0., 0.25],
                                       [0.25, 0., 0., 0., 0.75, 0., 0., 0.],
                                       [0., 0.25, 0., 0., 0., 0.75, 0., 0.],
                                       [0., 0., 0.25, 0., 0., 0., 0.75, 0.],
                                       [0., 0., 0., 0.25, 0., 0., 0., 0.75]])
        network.structure_matrix = np.array([[0., 1., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 1., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [1., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 1., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 1., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 1., 0.]])
        network.input_matrix = np.array([[0, 0],
                                         [0, 0],
                                         [1, 0],
                                         [0, 0],
                                         [0, 1],
                                         [0, 0],
                                         [0, 0],
                                         [0, 0]])
        network.output_matrix = np.asarray([[0, 0, 0, 1, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 1]])
        np.testing.assert_array_almost_equal(network.temperature_matrix[1], np.array([[60.],
                                                                                      [73.33333333],
                                                                                      [86.66666667],
                                                                                      [60.],
                                                                                      [33.33333333],
                                                                                      [46.66666667],
                                                                                      [60.],
                                                                                      [60.]]) + 273.15, decimal=5)
        np.testing.assert_array_equal(network.temperature_outputs[1], np.array([[60], [60]]) + 273.15)
        np.testing.assert_array_almost_equal(network.network_characteristics, np.array([[0.5, 0.5],
                                                                                        [0.5, 0.5]]), decimal=5)

    def test_output(self):
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 20), 1)
        flow_2 = Flow(Fluid("Water", temperature=273.15 + 100), 1)
        flows = [flow_1, flow_2]
        network = ExchangerNetwork(flows)
        network.phi_matrix = np.array([[0.75, 0., 0., 0., 0.25, 0., 0., 0.],
                                       [0., 0.75, 0., 0., 0., 0.25, 0., 0.],
                                       [0., 0., 0.75, 0., 0., 0., 0.25, 0.],
                                       [0., 0., 0., 0.75, 0., 0., 0., 0.25],
                                       [0.25, 0., 0., 0., 0.75, 0., 0., 0.],
                                       [0., 0.25, 0., 0., 0., 0.75, 0., 0.],
                                       [0., 0., 0.25, 0., 0., 0., 0.75, 0.],
                                       [0., 0., 0., 0.25, 0., 0., 0., 0.75]])
        network.structure_matrix = np.array([[0., 1., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 1., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [1., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 1, 0., 0., 0.],
                                             [0., 0., 0., 0., 0, 1., 0., 0.],
                                             [0., 0., 0., 0., 0., 0, 1., 0.]])
        network.input_matrix = np.array([[0, 0],
                                         [0, 0],
                                         [1, 0],
                                         [0, 0],
                                         [0, 1],
                                         [0, 0],
                                         [0, 0],
                                         [0, 0]])
        network.output_matrix = np.asarray([[0, 0, 0, 1, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 1]])
        print(network.temperature_outputs[1]-273.15)

    def test_output_3(self):
        flow_1 = Flow(Fluid("Water", temperature=373), 1)
        flow_2 = Flow(Fluid("Water", temperature=405), 1)
        flow_3 = Flow(Fluid("Water", temperature=293), 1)
        flows = [flow_1, flow_2, flow_3]
        network = ExchangerNetwork(flows)
        network.phi_matrix = np.array([[0.2, 0., 0., 0., 0.8, 0., 0., 0.],
                                       [0., 0.4, 0., 0., 0., 0.6, 0., 0.],
                                       [0., 0., 0.24, 0., 0., 0., 0.76, 0.],
                                       [0., 0., 0., 0.36, 0., 0., 0., 0.64],
                                       [0.6, 0., 0., 0., 0.4, 0., 0., 0.],
                                       [0., 0.6, 0., 0., 0., 0.4, 0., 0.],
                                       [0., 0., 0.76, 0., 0., 0., 0.24, 0.],
                                       [0., 0., 0., 0.16, 0., 0., 0., 0.84]])
        network.structure_matrix = np.array([[0., 1., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 1., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 1, 0., 0., 0.],
                                             [0., 0., 0., 0., 1, 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.75, 0.25, 0.]])
        network.input_matrix = np.array([[0, 0, 0],
                                         [1, 0, 0],
                                         [0, 0, 0],
                                         [0, 1, 0],
                                         [0, 0, 1],
                                         [0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0]])
        network.output_matrix = np.asarray([[1, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 1, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 1]])
        np.testing.assert_array_equal(network.temperature_matrix[1], np.array([[303.],
                                                                               [343.],
                                                                               [335.],
                                                                               [373.],
                                                                               [323.],
                                                                               [353.],
                                                                               [361.],
                                                                               [363.]]))
        np.testing.assert_array_equal(network.temperature_outputs[1], np.array([[303.],
                                                                                [335.],
                                                                                [363.]]))

        np.testing.assert_array_almost_equal(network.network_characteristics, np.array([[0.125, 0., 0.875],
                                                                                        [0.38730, 0.09836, 0.51434],
                                                                                        [0.55943, 0.22541, 0.21516]]),
                                             decimal=5)

    def test_print(self):
        ex_1, ex_2 = init_ex()
        ex_1.heat_transferability = 100
        ex_2.heat_transferability = 200
        network = ExchangerNetwork()

        exchangers = [ex_2, ex_1]
        network.exchangers = exchangers
        print(network)

    def test_bspHue(self):
        flow_1 = Flow(Fluid("nHeptane", temperature=273.15 + 120), 1)
        flow_2 = Flow(Fluid("nHeptane", temperature=273.15 + 120), 1)
        flow_3 = Flow(Fluid("nHeptane", temperature=273.15 + 120), 1)
        flow_4 = Flow(Fluid("Water", temperature=273.15 + 15), 1)
        flows = [flow_1, flow_2, flow_3, flow_4]
        network = ExchangerNetwork(flows)
        network.phi_matrix = np.array([[0.392, 0., 0., 0.608, 0., 0.],
                                       [0., 0.403, 0., 0., 0.597, 0.],
                                       [0., 0., 0.395, 0., 0., 0.605],
                                       [0.048, 0., 0., 0.952, 0., 0.],
                                       [0., 0.047, 0., 0., 0.953, 0.],
                                       [0., 0., 0.048, 0., 0., 0.952]])
        network.structure_matrix = np.array([[0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 1., 0., 0.],
                                             [0., 0., 0., 0., 1., 0.]])
        network.input_matrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1],
                                         [0, 0, 0, 0],
                                         [0, 0, 0, 0]])
        network.output_matrix = np.asarray([[1, 0, 0, 0, 0, 0],
                                            [0, 1, 0, 0, 0, 0],
                                            [0, 0, 1, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 1]])

        print(network.temperature_matrix[1] - 273.15)

    def test_bspHue_mix(self):
        flow_1 = Flow(Fluid("nHeptane", temperature=273.15 + 120), 1)
        flow_2 = Flow(Fluid("nHeptane", temperature=273.15 + 120), 1)
        flow_3 = Flow(Fluid("nHeptane", temperature=273.15 + 120), 1)
        flow_4 = Flow(Fluid("Water", temperature=273.15 + 15), 1)
        # flows = [flow_1, flow_2,flow_3,flow_4]
        flows = [flow_1, flow_4]
        network = ExchangerNetwork(flows)
        network.phi_matrix = np.array([[0.392, 0., 0., 0.608, 0., 0.],
                                       [0., 0.403, 0., 0., 0.597, 0.],
                                       [0., 0., 0.395, 0., 0., 0.605],
                                       [0.048, 0., 0., 0.952, 0., 0.],
                                       [0., 0.047, 0., 0., 0.953, 0.],
                                       [0., 0., 0.048, 0., 0., 0.952]])
        network.structure_matrix = np.array([[0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 0., 0., 0.],
                                             [0., 0., 0., 1., 0., 0.],
                                             [0., 0., 0., 0., 1., 0.]])
        """network.input_matrix = np.array([[1, 0, 0, 0],
                                         [0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1],
                                         [0, 0, 0, 0],
                                         [0, 0, 0, 0]])
        network.output_matrix = np.asarray([[1/3, 0, 0, 0, 0, 0],
                                            [0, 1/3, 0, 0, 0, 0],
                                            [0, 0, 1/3, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 1]])
        """
        network.input_matrix = np.array([[1, 0],
                                         [1, 0],
                                         [1, 0],
                                         [0, 1],
                                         [0, 0],
                                         [0, 0]])
        network.output_matrix = np.asarray([[1 / 3, 1 / 3, 1 / 3, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 1]])

        print(network.temperature_outputs[1] - 273.15)


if __name__ == '__main__':
    unittest.main()
