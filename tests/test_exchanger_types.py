import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import exchanger
from exchanger.exchanger import CounterCurrentFlow, CrossFlowOneRow
from exchanger.exchanger_types import *
from exchanger.stream import Fluid, Flow
from exchanger.parts import *
import exchanger.network as exnet


def init_extype():
    kA = 4000
    W = 3500
    fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.specific_heat)
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.specific_heat)

    ex = ExchangerEqualCells((2, 2), 'CrossFlowOneRow', flow_1=flow_1, flow_2=flow_2, total_transferability=kA)
    ex.flow_order_1 = 'dr2u'
    ex.flow_order_2 = 'ul2r'
    return ex


class ExchangerTypesTest(unittest.TestCase):

    def test_exchangertwoflow_init(self):
        ex_layout = ExchangerTwoFlow()
        ex_layout.auto_adjust = False
        self.assertEqual(ex_layout.cell_numbers, 0)
        self.assertEqual(ex_layout.input_flows, [NotImplemented, NotImplemented])
        self.assertEqual(ex_layout.output_flows, [NotImplemented, NotImplemented])
        self.assertEqual(ex_layout.exchangers, NotImplemented)
        self.assertEqual(ex_layout.flow_order_1, None)
        self.assertEqual(ex_layout.flow_order_2, None)
        self.assertEqual(ex_layout.layout_matrix, None)

        flow_1 = Flow(Fluid("Water", temperature=373), 1)
        flow_2 = Flow(Fluid("Water", temperature=405), 1)
        ex_layout = ExchangerTwoFlow(flow_1=flow_1, flow_2=flow_2)
        ex_layout.auto_adjust = False
        self.assertEqual(ex_layout.cell_numbers, 0)
        self.assertEqual(len(ex_layout.input_flows), 2)
        self.assertEqual(len(ex_layout.output_flows), 2)
        self.assertEqual(ex_layout.exchangers, NotImplemented)
        self.assertEqual(ex_layout.flow_order_1, None)
        self.assertEqual(ex_layout.flow_order_2, None)

        ex_1 = CounterCurrentFlow(flow_1.clone(), flow_2.clone())
        ex_2 = CrossFlowOneRow(flow_1.clone(), flow_2.clone())
        layout_matrix = np.array([ex_1, ex_2])
        ex_layout.layout_matrix = layout_matrix
        np.testing.assert_array_equal(ex_layout.layout_matrix, layout_matrix)
        self.assertEqual(len(str(ex_layout)), 119)
        layout_matrix = np.array([[ex_1, ex_2], [ex_2, ex_1]])
        ex_layout.layout_matrix = layout_matrix
        ex_layout.flow_order_1 = 'ul2d'
        ex_layout.flow_order_2 = 'ul2r'
        self.assertEqual(len(str(ex_layout)), 235)

    def test_flattening(self):
        flow_1 = Flow(Fluid("Water", temperature=10 + 273.15), 1)
        flow_2 = Flow(Fluid("Water", temperature=20 + 273.15), 1)
        flow_3 = Flow(Fluid("Water", temperature=30 + 273.15), 1)
        flow_4 = Flow(Fluid("Water", temperature=40 + 273.15), 1)
        ex_layout = ExchangerTwoFlow(flow_1=flow_1, flow_2=flow_2)

        ex_1 = CounterCurrentFlow(flow_1.clone(), flow_2.clone())
        ex_2 = CrossFlowOneRow(flow_3.clone(), flow_4.clone())
        ex_3 = CrossFlowOneRow(flow_1.clone(), flow_3.clone())
        ex_4 = CrossFlowOneRow(flow_2.clone(), flow_1.clone())

        layout_matrix = np.array([ex_1, ex_2])
        ex_layout.layout_matrix = layout_matrix
        np.testing.assert_array_equal(ex_layout.layout_matrix, layout_matrix)
        ex_layout.flow_order_1 = 'ul2d'
        ex_layout.flow_order_2 = 'ur2l'
        self.assertEqual(ex_layout.out_flow_1.out_temperature, flow_3.out_temperature)
        self.assertEqual(ex_layout.out_flow_2.out_temperature, flow_2.in_fluid.temperature)

        layout_matrix = np.array([ex_1, ex_2, ex_3])
        ex_layout.layout_matrix = layout_matrix
        np.testing.assert_array_equal(ex_layout.layout_matrix, layout_matrix)
        self.assertEqual(ex_layout.out_flow_1.out_temperature, flow_1.out_temperature)
        self.assertEqual(ex_layout.out_flow_2.out_temperature, flow_2.in_fluid.temperature)

        layout_matrix = np.array([[ex_1, ex_2], [ex_3, ex_4]])
        ex_layout.layout_matrix = layout_matrix
        np.testing.assert_array_equal(ex_layout.layout_matrix, layout_matrix)
        self.assertEqual(ex_layout.out_flow_1.out_temperature, flow_3.out_temperature)
        self.assertEqual(ex_layout.out_flow_2.out_temperature, flow_1.in_fluid.temperature)

        layout_matrix = np.array([[ex_1], [ex_2], [ex_3]])
        ex_layout.layout_matrix = layout_matrix
        np.testing.assert_array_equal(ex_layout.layout_matrix, layout_matrix)
        self.assertEqual(ex_layout.out_flow_1.out_temperature, flow_1.out_temperature)
        self.assertEqual(ex_layout.out_flow_2.out_temperature, flow_3.in_fluid.temperature)

    def test_equalcells_init(self):
        ex_layout = ExchangerEqualCells((2, 2))
        self.assertEqual(ex_layout.cell_numbers, 4)
        self.assertEqual(ex_layout.total_transferability, NotImplemented)
        self.assertEqual(ex_layout.input_flows, [NotImplemented, NotImplemented])
        self.assertEqual(ex_layout.output_flows, [NotImplemented, NotImplemented])
        self.assertEqual(ex_layout.exchangers, NotImplemented)

        ex_layout = ExchangerEqualCells((2, 2), total_transferability=10)
        self.assertEqual(ex_layout.total_transferability, 10)

        shell = SquareShellGeometry(5, 2, 1)
        pipe = StraightPipe(10, 13)
        pipe_layout = PipeLayout(pipe)
        assembly = Assembly(shell, pipe_layout)
        ex_layout = ExchangerEqualCells((2, 2), assembly=assembly, total_transferability=10)
        self.assertEqual(ex_layout.total_transferability, 10)

        assembly.heat_transfer_coefficient = 200
        with self.assertWarnsRegex(Warning,
                                   'defined value is not calculated, defined is returned',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertNotEqual(ex_layout.total_transferability, 35922, 0)
        ex_layout.total_transferability = NotImplemented

        self.assertNotEqual(ex_layout.total_transferability, 35922, 0)

    def test_equalcells_types(self):
        exchanger = ExchangerEqualCells()
        self.assertEqual(exchanger.exchangers_type, 'HeatExchanger')
        exchanger = ExchangerEqualCells(exchangers_type='ParallelFlow')
        self.assertEqual(exchanger.exchangers_type, 'ParallelFlow')
        with self.assertRaises(NotImplementedError):
            exchanger = ExchangerEqualCells(exchangers_type='Test')

    def test_equalcells_fill(self):
        exchangers = ExchangerEqualCells(exchangers_type='ParallelFlow')
        exchangers._fill()
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = Flow(Fluid("Air"), 1)
        exchangers.in_flow_1 = flow_1
        self.assertEqual(exchangers.input_flows, [flow_1, NotImplemented])

        self.assertEqual(exchangers.output_flows, [NotImplemented, NotImplemented])
        exchangers.in_flow_2 = flow_2
        self.assertEqual(exchangers.cell_numbers, 0)
        self.assertEqual(exchangers.shape, (0, 0))
        self.assertEqual(exchangers.exchangers, NotImplemented)
        self.assertEqual(len(exchangers.input_flows), 2)
        self.assertEqual(len(exchangers.output_flows), 2)

        exchangers._fill()
        exchangers.total_transferability = 3500
        exchangers._fill()
        exchangers.shape = (1, 1)
        exchangers._fill()
        self.assertEqual(exchangers.cell_numbers, 1)
        self.assertEqual(exchangers.shape, (1, 1))
        self.assertEqual(exchangers.exchangers, NotImplemented)
        self.assertEqual(len(exchangers.input_flows), 2)
        self.assertEqual(len(exchangers.output_flows), 2)

    def test_equalcells_calc(self):
        kA = 4000
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        ex = ExchangerEqualCells((2, 2), 'CrossFlowOneRow', flow_1=flow_1, flow_2=flow_2, total_transferability=kA)
        ex.flow_order_1 = 'dr2u'
        ex.flow_order_2 = 'ul2r'
        temp_check = np.array([[61.8],
                               [58.1]]) + 273.15
        np.testing.assert_array_almost_equal(ex.temperature_outputs[1], temp_check, decimal=1)

    def test_equalcells_calc_assembly(self):
        kA = 4000
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        shell = SquareShellGeometry(5, 2, 1)
        pipe = StraightPipe(10, 13)
        pipe_layout = PipeLayout(pipe)
        assembly = Assembly(shell, pipe_layout)
        assembly.heat_transfer_coefficient = 22.271
        ex = ExchangerEqualCells((2, 2), 'CrossFlowOneRow', flow_1=flow_1, flow_2=flow_2, assembly=assembly)
        self.assertAlmostEqual(ex.total_transferability, 4000, 0)
        ex.flow_order_1 = 'dr2u'
        ex.flow_order_2 = 'ul2r'
        ex.auto_adjust = False
        str(ex)
        self.assertEqual(ex.out_flow_1.mean_fluid.temperature, 100 + 273.15)
        self.assertEqual(ex.out_flow_2.mean_fluid.temperature, 20 + 273.15)
        ex.auto_adjust = True
        str(ex)
        self.assertAlmostEqual(ex.out_flow_1.mean_fluid.temperature, 62.18 + 273.15, 2)
        self.assertAlmostEqual(ex.out_flow_2.mean_fluid.temperature, 58.42 + 273.15, 2)

    def test_calc(self):
        ex = init_extype()
        self.assertEqual(ex.total_transferability, 4000)

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
        temp_check = np.array([[61.8],
                               [58.1]]) + 273.15
        np.testing.assert_array_almost_equal(ex.temperature_outputs[1], temp_check, decimal=1)
        ex._adjust_temperatures()
        self.assertAlmostEqual(ex.out_flow_1.mean_fluid.temperature, 61.8 + 273.15, delta=1)
        self.assertAlmostEqual(ex.out_flow_2.mean_fluid.temperature, 58.1 + 273.15, delta=1)

    def test_temp_adjustment_progress(self):
        ex = init_extype()
        ex._adjust_temperatures(5)
        ex.vis_temperature_adjustment_development()
        # plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_flow_temp_vis(self):
        ex = init_extype()
        ex.vis_flow_temperature_development()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

        ex._adjust_temperatures(5)

        ex.vis_flow_temperature_development()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_shapes(self):
        kA = 4000
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        ex = ExchangerEqualCells((3, 10), 'CounterCurrentFlow',
                                 flow_1=flow_1, flow_order_1='ul2d',
                                 flow_2=flow_2, flow_order_2='dr2l', total_transferability=kA)
        np.testing.assert_array_almost_equal(ex.temperature_outputs[1] - 273.15, np.array([[61.07],
                                                                                           [59.56]]), decimal=-1)
        ex._adjust_temperatures(5)
        np.testing.assert_array_almost_equal(ex.temperature_outputs[1] - 273.15, np.array([[61.07],
                                                                                           [59.56]]), decimal=2)

        ex.vis_flow_temperature_development()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

        ex.vis_heat_flux()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_print(self):
        ex = init_extype()
        ex._adjust_temperatures()
        self.assertEqual(len(ex.extended_info()), 3995)

    def test_autoadjust(self):
        ex = init_extype()
        ex.auto_adjust = False
        str(ex)
        self.assertAlmostEqual(ex.out_flow_1.mean_fluid.temperature, 100 + 273.15, delta=1)
        self.assertAlmostEqual(ex.out_flow_2.mean_fluid.temperature, 20 + 273.15, delta=1)
        ex = init_extype()
        str(ex)
        self.assertAlmostEqual(ex.out_flow_1.mean_fluid.temperature, 62.18 + 273.15, delta=1)
        self.assertAlmostEqual(ex.out_flow_2.mean_fluid.temperature, 58.42 + 273.15, delta=1)

    def test_input_change_after_init(self):
        ex = init_extype()
        temp = 363.15
        ex.flow_order_1 = 'ul2r'
        ex.flow_order_2 = 'dl2r'
        fld_1 = Fluid("Air", pressure=101420, temperature=temp)
        flow_1 = Flow(fld_1, 3500 / fld_1.specific_heat)
        ex.in_flow_1 = flow_1
        ex._adjust_temperatures()
        self.assertEqual(ex.in_flow_1.mean_fluid.temperature, temp)
        self.assertEqual(ex.layout_matrix[0, 0].flow_1.in_fluid.temperature, temp)

    def test_heat_flux_vis(self):
        ex = init_extype()
        ex._adjust_temperatures()

        ex.vis_heat_flux()
        # plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_vis_flow_direction(self):
        kA = 4000
        W = 3500
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, W / fld_1.specific_heat)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, W / fld_2.specific_heat)

        ex = ExchangerEqualCells((3, 3), 'CrossFlowOneRow', flow_1=flow_1, flow_2=flow_2, total_transferability=kA)
        ex.flow_order_1 = 'dr2u'
        ex.flow_order_2 = 'dl2r'
        ex._adjust_temperatures()
        ex.vis_heat_flux()
        #plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_input_arrangements(self):
        networks = []
        for inp in ExchangerTwoFlow.input_arrangements():
            netw = init_extype()
            netw.flow_order_1 = inp[0]
            netw.flow_order_2 = inp[1]
            netw._adjust_temperatures()
            networks.append(netw)

        ax_parameters_heat = {'vmin': 0, 'vmax': max([heat_flux_repr(netw.layout_matrix).max() for netw in networks])}
        exnet.vis_setups(networks, 'vis_heat_flux', fig_title='heat flows', **ax_parameters_heat)
        # plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")
        exnet.vis_setups(networks, 'vis_flow_temperature_development', fig_title='temperature development')
        # plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_vis_setup(self):
        networks = [init_extype(), init_extype(), init_extype(), init_extype(), init_extype(), init_extype(),
                    init_extype()]
        networks[-1].flow_order_1 = 'dr2l'
        networks[-2].in_flow_1.in_fluid.temperature = 273.15 + 50
        networks[-2].in_flow_1.out_fluid.temperature = 273.15 + 50
        networks[-2]._fill()
        networks[-2]._flatten()
        for n in networks:
            n._adjust_temperatures(5)

        ax_parameters_heat = {'vmin': 0, 'vmax': max([heat_flux_repr(netw.layout_matrix).max() for netw in networks])}

        exnet.vis_setups(networks, 'vis_heat_flux', fig_title='heat flows', **ax_parameters_heat)
        # plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")
        exnet.vis_setups(networks, 'vis_flow_temperature_development', fig_title='temperature development')
        # plt.show()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")


if __name__ == '__main__':
    unittest.main()
