import unittest
from exchanger.stream import *
from exchanger.parts import *
from exchanger.exchanger_creator import *
import matplotlib.pyplot as plt
from exchanger import *


def init_assembly():
    shell = SquareShellGeometry(5, 2, 1)
    pipe = StraightPipe(10e-3, 13e-3)
    pipe_layout = PipeLayout(pipe, 5)
    inlets = Inlets('ul', 'dl')
    assembly = Assembly(shell, pipe_layout, inlets=inlets)
    assembly.heat_transfer_coefficient = 4453.86
    return assembly


def init_fluids():
    W = 3500
    fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
    flow_1 = Flow(fld_1, W / fld_1.specific_heat)
    fld_2 = Fluid("Water", temperature=293.15)
    flow_2 = Flow(fld_2, W / fld_2.specific_heat)
    return flow_1, flow_2


class TestExchangerCreator(unittest.TestCase):
    def test_auto_create(self):
        assembly = init_assembly()
        flow_1, flow_2 = init_fluids()
        ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)
        self.assertEqual(ex_layout.shape, (1, 1))
        self.assertEqual(len(ex_layout.exchangers), 1)
        self.assertEqual(len(ex_layout.input_flows), 2)
        self.assertEqual(len(ex_layout.output_flows), 2)
        self.assertEqual(ex_layout.flow_order_1, 'ul2d')
        self.assertEqual(ex_layout.flow_order_2, 'dl2r')

    def test_baffles(self):
        assembly = init_assembly()
        baffle = SegmentalBaffle(1, 50)
        assembly.baffles = baffle
        flow_1, flow_2 = init_fluids()
        with self.assertRaises(ValueError,
                               msg='layout is created despite one vertical baffle with one tube pass is not possible'):
            ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)

    def test_tubepasses(self):
        assembly = init_assembly()
        assembly.tube_passes = 2
        flow_1, flow_2 = init_fluids()
        ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)

        self.assertEqual(ex_layout.shape, (2, 1))
        self.assertEqual(len(ex_layout.exchangers), 2)
        self.assertEqual(len(ex_layout.input_flows), 2)
        self.assertEqual(len(ex_layout.output_flows), 2)
        self.assertEqual(ex_layout.flow_order_1, 'ul2d')
        self.assertEqual(ex_layout.flow_order_2, 'dl2r')

        ex_layout.vis_heat_flow()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")
        ex_layout.vis_flow_temperature_development()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_tubepasses_baffles(self):
        assembly = init_assembly()
        assembly.tube_passes = 4
        baffle = SegmentalBaffle(5, 50)
        assembly.baffles = baffle
        flow_1, flow_2 = init_fluids()
        ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)
        self.assertEqual(ex_layout.shape, (4, 6))
        self.assertEqual(len(ex_layout.exchangers), 24)
        self.assertEqual(len(ex_layout.input_flows), 2)
        self.assertEqual(len(ex_layout.output_flows), 2)
        self.assertEqual(ex_layout.flow_order_1, 'ul2d')
        self.assertEqual(ex_layout.flow_order_2, 'dl2r')

        ex_layout.vis_heat_flow()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")
        ex_layout.vis_flow_temperature_development()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")

    def test_parallel_flow(self):
        fld_1 = Fluid("Water", pressure=101420, temperature=373.15)
        flow_1 = Flow(fld_1, 1)
        fld_2 = Fluid("Water", temperature=293.15)
        flow_2 = Flow(fld_2, 2)
        assembly = init_assembly()
        assembly.flow_orders = Inlets('dr', 'dl')

        assembly.tube_passes = 2
        baffle = SegmentalBaffle(15, 50)
        assembly.baffles = baffle
        ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)
        self.assertEqual(ex_layout.shape, (2, 16))
        self.assertEqual(len(ex_layout.exchangers), 32)
        self.assertEqual(len(ex_layout.input_flows), 2)
        self.assertEqual(len(ex_layout.output_flows), 2)
        self.assertEqual(ex_layout.flow_order_1, 'dr2u')
        self.assertEqual(ex_layout.flow_order_2, 'dl2r')

        ex_layout.vis_heat_flow()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")
        ex_layout.vis_flow_temperature_development()
        self.assertTrue(len(plt.gcf().get_axes()) > 0, "plot wasn't created")


if __name__ == '__main__':
    unittest.main()
