import unittest

import pyfluids


class FluidTests(unittest.TestCase):
    from pyfluids import Fluid as fldFluid
    from pyfluids import Mixture as fldMixture
    from stream import Fluid, Flow

    def test_fluid_init(self):
        with self.assertRaises(TypeError):
            fluid = self.Fluid()
        fluid = self.Fluid("Water")
        self.assertEqual(fluid.title, "Water")

        self.assertEqual(fluid.fluid.units_system, pyfluids.UnitsSystem.SI)

        fluid = self.Fluid("Water", temperature=300)
        self.assertEqual(fluid.temperature, 300)

        fluid = self.Fluid("Water", pressure=300)
        self.assertEqual(fluid.pressure, 300)

        fluid = self.Fluid("Water", temperature=350, pressure=100)
        self.assertEqual(fluid.temperature, 350)
        self.assertEqual(fluid.pressure, 100)

    def test_fluid_instance(self):
        fluid = self.Fluid("Water")
        self.assertEqual(fluid.instance, self.fldFluid)
        self.assertIsInstance(fluid.fluid, self.fldFluid)

        fluid = self.Fluid("Water", instance='Fluid')
        self.assertEqual(fluid.instance, self.fldFluid)
        self.assertIsInstance(fluid.fluid, self.fldFluid)

        # @TODO implement Mixture and HumidAir
        with self.assertRaises(AttributeError):
            fluid = self.Fluid("Water", instance='Mixture')
            # self.assertEqual(fluid._instance, self.fldMixture)
            # self.assertIsInstance(fluid._fluid, self.fldMixture)

        with self.assertRaises(AttributeError):
            fluid = self.Fluid("Water", instance='Test')

    def test_fluid_pressure(self):
        fluid = self.Fluid("Water")
        self.assertEqual(fluid.pressure, 101325)

        fluid.pressure = 10
        self.assertEqual(fluid.pressure, 10)

    def test_fluid_temperature(self):
        fluid = self.Fluid("Air")
        self.assertEqual(fluid.temperature, 293.15)

        value = 60
        fluid.temperature = value
        self.assertEqual(fluid.temperature, value)

        fluid = self.Fluid("Water")
        fluid.temperature = 60
        self.assertEqual(fluid.temperature, 293.15)

    def test_fluid_print(self):
        fluid = self.Fluid("Water")
        fluid.temperature = 350
        fluid.pressure = 10
        print(fluid)

    def test_fluid_clone(self):
        fluid = self.Fluid("Water")
        new_fluid = fluid.clone()
        self.assertNotEqual(fluid, new_fluid)
        new_fluid.pressure = 100e3

        fluid = self.Fluid("Water", temperature=280)
        new_fluid = fluid.clone()
        self.assertNotEqual(fluid, new_fluid)
        new_fluid.pressure = 100e3
        new_fluid.temperature = 350
        fluid.pressure = 150e3

        self.assertEqual(fluid.temperature, 280)
        self.assertEqual(new_fluid.temperature, 350)
        self.assertEqual(fluid.pressure, 150e3)
        self.assertEqual(new_fluid.pressure, 100e3)

    def test_flow_init(self):
        with self.assertRaises(TypeError):
            flow = self.Fluid()
        fluid = self.Fluid("Water")
        flow = self.Flow(fluid)
        self.assertEqual(flow.in_fluid, fluid)

        flow.volume_flow = 10
        self.assertEqual(flow.volume_flow, 10)

        flow.mass_flow = 15
        self.assertEqual(flow.mass_flow, 15)
        in_density = fluid.density
        self.assertEqual(flow.volume_flow, 15 / in_density)

    def test_flow_phasechange(self):
        fluid = self.Fluid("Water")
        flow = self.Flow(fluid, 15)
        flow.pressure_loss = -5000
        with self.assertRaises(Warning):
            flow.out_temperature = 250 + 273.15
        flow.out_temperature = 101 + 273.15

    def test_flow_heatflow(self):
        fluid = self.Fluid("Water", temperature=273.15 + 15)
        flow = self.Flow(fluid, 0.33)
        self.assertAlmostEqual(flow.heat_capacity_flow, 1382, 0)
        self.assertEqual(flow.heat_flow, 0)
        flow.out_temperature = 273.15 + 23.11
        self.assertAlmostEqual(flow.heat_flow, -11.2e3, delta=0.1e3)

    def test_flow_clone(self):
        fluid = self.Fluid("Water")
        flow = self.Flow(fluid, 1)
        new_flow = flow.clone()
        self.assertNotEqual(flow, new_flow)
        self.assertNotEqual(flow.in_fluid, new_flow.in_fluid)
        self.assertNotEqual(flow.mean_fluid, new_flow.mean_fluid)
        self.assertNotEqual(flow.out_fluid, new_flow.out_fluid)
        self.assertEqual(flow.mass_flow,new_flow.mass_flow)


    def test_flow_print(self):
        fluid = self.Fluid("Water", temperature=273.15 + 15)
        flow = self.Flow(fluid, 1)
        print(flow)
        flow.out_temperature = 273.15 + 99
        print(flow)



    """
    exchanger.py tests
    """
    from exchanger import HeatExchanger, ParallelFlow
    def test_exchanger_init(self):
        flow_1 = self.Flow(self.Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = self.Flow(self.Fluid("Air"), 1)
        ex = self.HeatExchanger(flow_1, flow_2)
        print(ex.part)
        print(ex)
        ex.heat_transferability = 560
        self.assertEqual(ex.heat_transferability, 560)
        self.assertAlmostEqual(ex.ntu[0], 0.405, 2)

    def test_exchanger_parallel(self):
        flow_1 = self.Flow(self.Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = self.Flow(self.Fluid("Air"), 1)
        part = self.Part(560)
        ex = self.ParallelFlow(flow_1, flow_2, part)
        p = ex.p
        self.assertIsInstance(p, tuple)

    def test_exchanger_print(self):
        flow_1 = self.Flow(self.Fluid("Water", temperature=273.15 + 15), 0.33)
        flow_2 = self.Flow(self.Fluid("Air"), 1)
        part = self.Part(560)
        ex = self.ParallelFlow(flow_1, flow_2, part)
        print(ex)


if __name__ == '__main__':
    unittest.main()
