import unittest

from exchanger.stream import *
from exchanger.parts import *
from exchanger.exchanger import *
from exchanger.utils import *


class ExchangerTests(unittest.TestCase):
    def test_exchanger_init(self):
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = Flow(Fluid("Air"), 1)
        ex = HeatExchanger(flow_1, flow_2)
        print(ex.part)
        print(ex)
        ex.heat_transferability = 560
        self.assertEqual(ex.heat_transferability, 560)
        self.assertAlmostEqual(ex.ntu[0], 0.405, 2)
        print(ex)

    def test_exchanger_parallel(self):
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = Flow(Fluid("Air"), 1)
        part = Part(560)
        ex = ParallelFlow(flow_1, flow_2, part)
        p = ex.p
        self.assertIsInstance(p, tuple)

    def test_exchanger_print(self):
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = Flow(Fluid("Air"), 1)
        part = Part(560)
        ex = ParallelFlow(flow_1, flow_2, part)
        print(ex)

    def test_OneOuterThreeInnerTwoCounterflow(self):
        flow_outside = Flow(Fluid("Air", temperature=20 + 273.15), mass_flow=0.4)
        flow_inside = Flow(Fluid("Water", pressure=5e5, temperature=105 + 273.15), mass_flow=0.15)
        pipe = StraightPipe(diameter_in=11.9e-3, diameter_out=12e-3, length=3.233)
        pipe_layout = PipeLayout(pipe, 5000)
        pipe_layout.heat_transfer_coefficient = 35
        ex = OneOuterThreeInnerTwoCounterflow(flow_outside, flow_inside, pipe_layout)
        print(ex)


if __name__ == '__main__':
    unittest.main()
