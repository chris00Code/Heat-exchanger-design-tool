import unittest
import numpy as np
from exchanger_types import ExchangerEqualCellsTwoFlow
from stream import Fluid, Flow


def init_extype():
    kA = 4749
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
        temp_check = np.array([[60.],
                               [60.]]) + 273.15
        np.testing.assert_array_almost_equal(ex.temperature_outputs[1], temp_check, decimal=2)

    def test_calc(self):
        ex = init_extype()
        self.assertEqual(ex.transferability, 4749)

        phi_check = np.array([[0.75, 0., 0., 0., 0.25, 0., 0., 0.],
                              [0., 0.75, 0., 0., 0., 0.25, 0., 0.],
                              [0., 0., 0.75, 0., 0., 0., 0.25, 0.],
                              [0., 0., 0., 0.75, 0., 0., 0., 0.25],
                              [0.25, 0., 0., 0., 0.75, 0., 0., 0.],
                              [0., 0.25, 0., 0., 0., 0.75, 0., 0.],
                              [0., 0., 0.25, 0., 0., 0., 0.75, 0.],
                              [0., 0., 0., 0.25, 0., 0., 0., 0.75]])

        phi = ex.phi_matrix
        np.testing.assert_array_almost_equal(phi, phi_check, decimal=2)


if __name__ == '__main__':
    unittest.main()
