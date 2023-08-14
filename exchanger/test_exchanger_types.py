import unittest
import numpy as np
from exchanger_types import ExchangerEqualCellsTwoFlow
from stream import Fluid, Flow


def init_extype():
    kA = 4000
    W = 3500
    fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.specific_heat)
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.specific_heat)

    ex = ExchangerEqualCellsTwoFlow((2, 2), 'CrossFlowOneRow', flow_1, flow_2, kA)
    ex.order_1 = 'dr2u'
    ex.order_2 = 'ul2r'
    return ex



class ExchangerTypesTest(unittest.TestCase):

    def test_init(self):
        ex = ExchangerEqualCellsTwoFlow()
        self.assertEqual(ex.cell_numbers, 0)
        self.assertEqual(len(ex.input_flows), 0)
        self.assertEqual(len(ex.output_flows), 0)
        self.assertEqual(len(ex.exchangers), 0)

        flow_1 = Flow(Fluid("Water", temperature=373), 1)
        flow_2 = Flow(Fluid("Water", temperature=405), 1)
        ex = ExchangerEqualCellsTwoFlow(flow_1=flow_1, flow_2=flow_2)
        self.assertEqual(ex.cell_numbers, 0)
        self.assertEqual(len(ex.input_flows), 2)
        self.assertEqual(len(ex.exchangers), 0)

    def test_init_and_calc(self):
        ex = init_extype()
        temp_check = np.array([[61.8],
                               [58.1]]) + 273.15
        np.testing.assert_array_almost_equal(ex.temperature_outputs[1], temp_check, decimal=1)

    def test_calc(self):
        ex = init_extype()
        self.assertEqual(ex.transferability, 4000)

        phi_check = np.array([[0.78, 0., 0., 0., 0.22, 0., 0., 0.],
                              [0., 0.78, 0., 0., 0., 0.22, 0., 0.],
                              [0., 0., 0.78, 0., 0., 0., 0.22, 0.],
                              [0., 0., 0., 0.78, 0., 0., 0., 0.22],
                              [0.22, 0., 0., 0., 0.78, 0., 0., 0.],
                              [0., 0.22, 0., 0., 0., 0.78, 0., 0.],
                              [0., 0., 0.22, 0., 0., 0., 0.78, 0.],
                              [0., 0., 0., 0.22, 0., 0., 0., 0.78]])

        phi = ex.phi_matrix
        np.testing.assert_array_almost_equal(phi, phi_check, decimal=2)

    def test_temp_adjust(self):
        ex = init_extype()
        #print(ex)
        ex._adjust_temperatures(15)
        print(ex)

    def test_shapes(self):
        kA = 4000
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        ex = ExchangerEqualCellsTwoFlow((10, 10), 'CrossFlowOneRow', flow_1, flow_2, kA)
        ex.order_1 = 'ul2d'
        ex.order_2 = 'ul2r'
        print(ex.temperature_outputs[1]-273.15)
        ex._adjust_temperatures(1)
        print(ex.temperature_outputs[1]-273.15)

    def test_typedifferent(self):
        kA = 4749
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        ex = ExchangerEqualCellsTwoFlow((2, 2), 'ParallelFlow', flow_1, flow_2, kA)
        ex.order_1 = 'dr2u'
        ex.order_2 = 'ul2r'
        print(ex.temperature_outputs[1]-273.15)

    def test_print(self):
        ex = init_extype()
        ex._adjust_temperatures()
        print(ex)
        print(ex.network_characteristics)
        print(ex.extended_info())

    def test_heat_flow_vis(self):
        ex = init_extype()
        ex._adjust_temperatures()
        ex.heat_flow_vis()
        #print(ex.heat_flow_vis())

if __name__ == '__main__':
    unittest.main()
