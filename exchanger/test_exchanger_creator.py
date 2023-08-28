import unittest
from stream import *
from parts import *
from exchanger_creator import *
import matplotlib.pyplot as plt


def init_assembly():
    shell = SquareShellGeometry(5, 2, 1)
    pipe = StraightPipe(10e-3, 13e-3)
    pipe.heat_transfer_coefficient = 200
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
        # print(ex_layout.extended_info())
        print(ex_layout)

    def test_baffles(self):
        assembly = init_assembly()
        baffle = SegmentalBaffle(1, 50)
        assembly.baffles = baffle
        print(assembly)
        flow_1, flow_2 = init_fluids()
        with self.assertRaises(ValueError):
            ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)

    def test_tubepasses(self):
        assembly = init_assembly()
        assembly.tube_passes = 2
        flow_1, flow_2 = init_fluids()
        ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)
        print(ex_layout.extended_info())

        ex_layout.vis_heat_flow()
        ex_layout.vis_flow_temperature_development()
        plt.show()

    def test_tubepasses_baffles(self):
        assembly = init_assembly()
        assembly.tube_passes = 4
        baffle = SegmentalBaffle(5, 50)
        assembly.baffles = baffle
        flow_1, flow_2 = init_fluids()
        ex_layout = auto_create_exchanger(flow_1, flow_2, assembly)
        ex_layout.flow_order_2 ='ul2d'
        print(ex_layout.flow_orders_str())
        print(ex_layout.extended_info())

        ex_layout.vis_heat_flow()
        ex_layout.vis_flow_temperature_development()
        plt.show()


if __name__ == '__main__':
    unittest.main()
