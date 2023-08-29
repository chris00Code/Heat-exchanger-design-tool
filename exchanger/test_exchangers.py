import unittest

from stream import *
from parts import *
import exchanger
from exchanger import *
from utils import *

class ExchangerTests(unittest.TestCase):

    def test_available_classes(self):
        available_classes = get_available_class_names(exchanger)


    def test_exchanger_init(self):
        flow_1 = Flow(Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = Flow(Fluid("Air"), 1)
        ex = HeatExchanger(flow_1, flow_2)
        print(ex.part)
        print(ex)
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
        print(ex)


if __name__ == '__main__':
    unittest.main()
