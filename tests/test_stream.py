import unittest
import pyfluids as pyf
from exchanger.stream import Fluid, Flow


class FluidTests(unittest.TestCase):

    def test_fluid_init(self):
        with self.assertRaises(TypeError, msg='Fluid instance was created with no parameter'):
            fluid = Fluid()
        fluid = Fluid("Water")
        self.assertEqual(fluid.title, "Water")

        self.assertEqual(fluid.fluid.units_system, pyf.UnitsSystem.SI)

        fluid = Fluid("Water", temperature=300)
        self.assertEqual(fluid.temperature, 300)

        fluid = Fluid("Water", pressure=300)
        self.assertEqual(fluid.pressure, 300)

        fluid = Fluid("Water", temperature=350, pressure=100)
        self.assertEqual(fluid.temperature, 350)
        self.assertEqual(fluid.pressure, 100)

    def test_fluid_instance(self):
        fluid = Fluid("Water")
        self.assertEqual(fluid.instance, pyf.Fluid)
        self.assertIsInstance(fluid.fluid, pyf.Fluid)

        fluid = Fluid("Water", instance='Fluid')
        self.assertEqual(fluid.instance, pyf.Fluid)
        self.assertIsInstance(fluid.fluid, pyf.Fluid)

        with self.assertRaisesRegex(AttributeError, 'instance \'Mixture\' not implemented'):
            fluid = Fluid("Water", instance='Mixture')
        with self.assertRaisesRegex(AttributeError, 'instance \'HumidAir\' not implemented'):
            fluid = Fluid("Water", instance='HumidAir')
        with self.assertRaisesRegex(AttributeError, 'instance \'Test\' not implemented'):
            fluid = Fluid("Water", instance='Test')

    def test_fluid_pressure(self):
        fluid = Fluid("Water")
        self.assertEqual(fluid.pressure, 101325, msg='initial pressure value not 101325 Pa')

        fluid.pressure = 10
        self.assertEqual(fluid.pressure, 10, msg='pressure setting not working')

    def test_fluid_temperature(self):
        fluid = Fluid("Water")
        self.assertEqual(fluid.temperature, 293.15, msg='initial temperature not 293.15 °C')

        value = 280
        fluid.temperature = value
        self.assertEqual(fluid.temperature, value, msg='temperature setting not working')

        fluid = Fluid("Air")
        value = 60
        fluid.temperature = value
        self.assertEqual(fluid.temperature, value, msg='negative degree temperature setting not working')

    def test_fluid_print(self):
        fluid = Fluid("Water")
        fluid.temperature = 350
        fluid.pressure = 10
        print(fluid)

    def test_fluid_clone(self):
        fluid = Fluid("Water")
        new_fluid = fluid.clone()
        self.assertNotEqual(fluid, new_fluid)
        new_fluid.pressure = 100e3

        fluid = Fluid("Water", temperature=280)
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
            flow = Fluid()
        fluid = Fluid("Water")
        flow = Flow(fluid)
        self.assertEqual(flow.in_fluid, fluid)

        flow.volume_flow = 10
        self.assertEqual(flow.volume_flow, 10)

        flow.mass_flow = 15
        self.assertEqual(flow.mass_flow, 15)
        in_density = fluid.density
        self.assertEqual(flow.volume_flow, 15 / in_density)

    def test_flow_phasechange(self):
        fluid = Fluid("Water")
        flow = Flow(fluid, 15)
        flow.pressure_loss = -5000
        with self.assertRaises(Warning):
            flow.out_temperature = 250 + 273.15
        flow.out_temperature = 101 + 273.15

    def test_flow_heatflow(self):
        fluid = Fluid("Water", temperature=273.15 + 15)
        flow = Flow(fluid, 0.33)
        self.assertAlmostEqual(flow.heat_capacity_flow, 1382, 0)
        self.assertEqual(flow.heat_flow, 0)
        flow.out_temperature = 273.15 + 23.11
        self.assertAlmostEqual(flow.heat_flow, -11.2e3, delta=0.1e3)

    def test_flow_clone(self):
        fluid = Fluid("Water")
        flow = Flow(fluid, 1)
        new_flow = flow.clone()
        self.assertNotEqual(flow, new_flow)
        self.assertNotEqual(flow.in_fluid, new_flow.in_fluid)
        self.assertNotEqual(flow.mean_fluid, new_flow.mean_fluid)
        self.assertNotEqual(flow.out_fluid, new_flow.out_fluid)
        self.assertEqual(flow.mass_flow, new_flow.mass_flow)

    def test_flow_print(self):
        fluid = Fluid("Water", temperature=273.15 + 15)
        flow = Flow(fluid, 1)
        print(flow)
        flow.out_temperature = 273.15 + 99
        print(flow)


if __name__ == '__main__':
    unittest.main()
