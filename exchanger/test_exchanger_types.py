import unittest
import numpy as np
from exchanger import *
from exchanger_types import *
from stream import Fluid, Flow
from parts import *
import matplotlib.pyplot as plt
import matplotlib
from characteristic_plots import *


def init_extype():
    kA = 4000
    W = 3500
    fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.specific_heat)
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.specific_heat)

    ex = ExchangerEqualCellsTwoFlow((2, 2), 'CrossFlowOneRow', flow_1, flow_2, kA)
    ex.flow_order_1 = 'dr2u'
    ex.flow_order_2 = 'ul2r'
    return ex


def test_plot_setup():
    matplotlib.use('Agg')
    plt.close()


class ExchangerTypesTest(unittest.TestCase):

    def test_exchangertwoflow_init(self):
        ex_layout = ExchangerTwoFlow()
        self.assertEqual(ex_layout.cell_numbers, 0)
        self.assertEqual(ex_layout.input_flows, [NotImplemented, NotImplemented])
        self.assertEqual(ex_layout.output_flows, [NotImplemented, NotImplemented])
        self.assertEqual(len(ex_layout.exchangers), 0)
        self.assertEqual(ex_layout.flow_order_1, None)
        self.assertEqual(ex_layout.flow_order_2, None)
        self.assertEqual(ex_layout.layout_matrix, None)

        flow_1 = Flow(Fluid("Water", temperature=373), 1)
        flow_2 = Flow(Fluid("Water", temperature=405), 1)
        ex_layout = ExchangerTwoFlow(flow_1=flow_1, flow_2=flow_2)
        self.assertEqual(ex_layout.cell_numbers, 0)
        self.assertEqual(len(ex_layout.input_flows), 2)
        self.assertEqual(len(ex_layout.output_flows), 2)
        self.assertEqual(len(ex_layout.exchangers), 0)
        self.assertEqual(ex_layout.flow_order_1, None)
        self.assertEqual(ex_layout.flow_order_2, None)

        ex_1 = CounterCurrentFlow(flow_1.clone(), flow_2.clone())
        ex_2 = CrossFlowOneRow(flow_1.clone(), flow_2.clone())
        layout_matrix = np.array([ex_1, ex_2])
        ex_layout.layout_matrix = layout_matrix
        np.testing.assert_array_equal(ex_layout.layout_matrix, layout_matrix)
        print(ex_layout)

    def test_equalcells_init(self):
        ex_layout = ExchangerEqualCells((2, 2))
        self.assertEqual(ex_layout.cell_numbers, 4)
        self.assertEqual(ex_layout.total_transferability, None)
        self.assertEqual(ex_layout.input_flows, [NotImplemented, NotImplemented])
        self.assertEqual(ex_layout.output_flows, [NotImplemented, NotImplemented])
        self.assertEqual(len(ex_layout.exchangers), 0)

        ex_layout = ExchangerEqualCells((2, 2), total_transferability=10)
        self.assertEqual(ex_layout.total_transferability, 10)

        shell = SquareShell(5, 2, 1)
        pipe = StraightPipe(10, 13)
        pipe_layout = PipeLayout(pipe)
        assembly = Assembly(shell, pipe_layout)
        ex_layout = ExchangerEqualCells((2, 2), assembly=assembly, total_transferability=10)
        self.assertEqual(ex_layout.total_transferability, 10)

        assembly.heat_transfer_coefficient = 200
        self.assertAlmostEqual(ex_layout.total_transferability, 35922, 0)

    def test_equalcells_types(self):
        exchanger = ExchangerEqualCells()
        self.assertEqual(exchanger.exchangers_type, 'HeatExchanger')
        exchanger = ExchangerEqualCells(exchangers_type='ParallelFlow')
        self.assertEqual(exchanger.exchangers_type, 'ParallelFlow')
        with self.assertRaises(NotImplementedError):
            exchanger = ExchangerEqualCells(exchangers_type='Test')

    def test_equalcells_fill(self):
        exchangers = ExchangerEqualCells(exchangers_type='ParallelFlow')
        with self.assertRaises(ValueError):
            exchangers._fill()

        flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = Flow(Fluid("Air"), 1)
        exchangers.in_flow_1 = flow_1
        print(exchangers.input_flows)

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
        # print(ex)
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
        ex.flow_order_1 = 'ul2d'
        ex.flow_order_2 = 'ul2r'
        print(ex.temperature_outputs[1] - 273.15)
        ex._adjust_temperatures(1)
        print(ex.temperature_outputs[1] - 273.15)

    def test_typedifferent(self):
        kA = 4749
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        ex = ExchangerEqualCellsTwoFlow((2, 2), 'CounterCurrentFlow', flow_1, flow_2, kA)
        ex.flow_order_1 = 'ur2d'
        ex.flow_order_2 = 'ul2r'
        print(ex.temperature_outputs[1] - 273.15)
        ex._adjust_temperatures()
        ex.heat_flow_vis()
        print(ex.extended_info())

    def test_print(self):
        ex = init_extype()
        ex._adjust_temperatures()
        print(ex)
        print(ex.network_characteristics)
        print(ex.extended_info())

    def test_heat_flow_vis(self):
        ex = init_extype()
        ex._adjust_temperatures()
        test_plot_setup()
        ex.heat_flow_vis()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")


if __name__ == '__main__':
    unittest.main()
