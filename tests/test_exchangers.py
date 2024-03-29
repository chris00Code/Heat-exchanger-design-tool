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
        ex.heat_transferability = 560
        self.assertEqual(ex.heat_transferability, 560)
        self.assertAlmostEqual(ex.ntu[0], 0.405, 2)


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


    def test_OneOuterThreeInnerTwoCounterflow(self):
        flow_outside = Flow(Fluid("Air", temperature=20 + 273.15), mass_flow=0.4)
        flow_inside = Flow(Fluid("Water", pressure=5e5, temperature=105 + 273.15), mass_flow=0.15)
        pipe = StraightPipe(diameter_in=11.9e-3, diameter_out=12e-3, length=3.233)
        pipe_layout = PipeLayout(pipe, 20)
        pipe_layout.heat_transfer_coefficient = 35
        ex = OneOuterThreeInnerTwoCounterFlow(flow_outside, flow_inside, pipe_layout)
        self.assertAlmostEqual(ex.p[0], 0.179, 2)
        pipe_layout.number_pipes = 5000
        self.assertAlmostEqual(ex.p[0], 0.935, 2)

        flow_inside = flow_outside
        ex = OneOuterThreeInnerTwoCounterFlow(flow_outside, flow_inside, pipe_layout)
        self.assertEqual(ex.r[0], 1.0)
        self.assertAlmostEqual(ex.p[0], 0.87, 2)


if __name__ == '__main__':
    unittest.main()
