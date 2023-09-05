import unittest
import pyfluids as pyf
from exchanger.stream import Fluid, Flow


class TestFluid(unittest.TestCase):

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

    def test_fluid_clone(self):
        fluid = Fluid("Water")
        new_fluid = fluid.clone()
        self.assertNotEqual(fluid, new_fluid, msg='fluid cloning not working, fluid has same hash value')
        new_fluid.pressure = 100e3

        fluid = Fluid("Water", temperature=280)
        new_fluid = fluid.clone()
        self.assertNotEqual(fluid, new_fluid, msg='fluid cloning not working, fluid has same hash value')
        new_fluid.pressure = 100e3
        new_fluid.temperature = 350
        fluid.pressure = 150e3

        self.assertEqual(fluid.temperature, 280, msg='fluid cloning not working, temperature is still same object')
        self.assertEqual(new_fluid.temperature, 350, msg='fluid cloning not working, temperature is still same object')
        self.assertEqual(fluid.pressure, 150e3, msg='fluid cloning not working, pressure is still same object')
        self.assertEqual(new_fluid.pressure, 100e3, msg='fluid cloning not working, pressure is still same object')


    def test_fluid_clone_constructor(self):
        fluid = Fluid("Water")
        new_fluid = Fluid(fluid=fluid)
        self.assertNotEqual(fluid, new_fluid, msg='fluid cloning not working, fluid has same hash value')
        new_fluid.pressure = 100e3

        fluid = Fluid("Water", temperature=280)
        new_fluid = fluid.clone()
        self.assertNotEqual(fluid, new_fluid, msg='fluid cloning not working, fluid has same hash value')
        new_fluid.pressure = 100e3
        new_fluid.temperature = 350
        fluid.pressure = 150e3

        self.assertEqual(fluid.temperature, 280, msg='fluid cloning not working, temperature is still same object')
        self.assertEqual(new_fluid.temperature, 350, msg='fluid cloning not working, temperature is still same object')
        self.assertEqual(fluid.pressure, 150e3, msg='fluid cloning not working, pressure is still same object')
        self.assertEqual(new_fluid.pressure, 100e3, msg='fluid cloning not working, pressure is still same object')

    def test_fluid_str(self):
        expected_output = r'^Fluid: title = \w+, id = \d+\n\tp = \d+(\.\d+)? Pa\n\tt = -?\d+(\.\d+)? °C'

        fluid = Fluid("Air", 210.20, 60)
        self.assertRegex(str(fluid), expected_output, msg='fluid str has not expected pattern')
        fluid = Fluid("Water")
        self.assertRegex(str(fluid), expected_output, msg='fluid str has not expected pattern')


class TestFlow(unittest.TestCase):
    def setUp(self):
        self.fluid_water = Fluid("Water")

    def test_flow_init(self):
        with self.assertRaises(TypeError, msg='Flow instance was created with no parameter'):
            flow = Fluid()

        flow = Flow(self.fluid_water)
        self.assertEqual(flow.in_fluid, self.fluid_water,
                         msg='in fluid object is not the same object as in the constructor assigned')

    def test_flow_rate(self):
        flow = Flow(self.fluid_water)
        flow.volume_flow = 10
        self.assertEqual(flow.volume_flow, 10, msg='volume flow setter is not working')

        value = 15
        flow.mass_flow = value
        self.assertEqual(flow.mass_flow, value, msg='mass flow setter is not working')
        in_density = self.fluid_water.density
        self.assertEqual(flow.volume_flow, value / in_density,
                         msg='volume flow calculating by mass flow and density not correct')

    def test_flow_phasechange(self):
        flow = Flow(self.fluid_water, 15)
        value = -5000
        flow.pressure_loss = value
        self.assertEqual(flow.in_fluid.pressure, 101325, msg='in fluid pressure not correct')
        self.assertEqual(flow.out_fluid.pressure, 101325 - value,
                         msg='out fluid pressure not correct calculated/set by pressure loss')
        with self.assertWarnsRegex(Warning, 'the phase changes, this could lead to some problems',
                                   msg='no warning when the phase change is set'):
            flow.out_temperature = 250 + 273.15
        with self.assertWarnsRegex(Warning, 'the phase changes, this could lead to some problems',
                                   msg='no warning when the phase change is used'):
            q = flow.heat_flow

        flow.out_temperature = 101 + 273.15
        q = flow.heat_flow

    def test_flow_heatflow(self):
        fluid = Fluid("Water", temperature=273.15 + 15)
        flow = Flow(fluid, 0.33)
        self.assertAlmostEqual(flow.heat_capacity_flow, 1382, 0, msg='heat capacity flow not correct')
        self.assertEqual(flow.in_fluid.temperature - flow.out_temperature, 0, msg='temperature delta is not 0')
        self.assertEqual(flow.heat_flow, 0, msg='heat flow is not 0, if temperature delta is 0')
        flow.out_temperature = 273.15 + 23.11
        self.assertNotEqual(flow.in_fluid.temperature - flow.out_temperature, 0, msg='temperature delta is 0')
        self.assertAlmostEqual(flow.heat_flow, -11.2e3, delta=0.1e3, msg='heat flow was not calculated correct')

    def test_flow_clone(self):
        fluid = Fluid("Water")
        flow = Flow(fluid, 1)
        new_flow = flow.clone()
        self.assertNotEqual(flow, new_flow, msg='cloned flow object is equal, has same hash value')
        self.assertNotEqual(flow.in_fluid, new_flow.in_fluid, msg='cloned in fluids are equal, have same hash values')
        self.assertNotEqual(flow.mean_fluid, new_flow.mean_fluid,
                            msg='cloned mean fluids are equal, have same hash values')
        self.assertNotEqual(flow.out_fluid, new_flow.out_fluid,
                            msg='cloned out fluids are equal, have same hash values')
        self.assertEqual(flow.mass_flow, new_flow.mass_flow, msg='mass flow was not cloned correct')


    def test_flow_clone_constructor(self):
        fluid = Fluid("Water")
        flow = Flow(fluid, 1)
        new_flow = Flow(flow=flow)
        self.assertNotEqual(flow, new_flow, msg='cloned flow object is equal, has same hash value')
        self.assertNotEqual(flow.in_fluid, new_flow.in_fluid, msg='cloned in fluids are equal, have same hash values')
        self.assertNotEqual(flow.mean_fluid, new_flow.mean_fluid,
                            msg='cloned mean fluids are equal, have same hash values')
        self.assertNotEqual(flow.out_fluid, new_flow.out_fluid,
                            msg='cloned out fluids are equal, have same hash values')
        self.assertEqual(flow.mass_flow, new_flow.mass_flow, msg='mass flow was not cloned correct')


def test_flow_print(self):
        expected_output = r'^Flow: id = \d+\n\tmass flow = \d+(\.\d+)? kg\/s\n' \
                          r'\theat capacity flow: W_dot = \d+(\.\d+)? W\/K\n' \
                          r'\theat flow: Q_dot = -?\d+(\.\d+)? kW\n\n' \
                          r'Input Fluid:\n.*\n.*\n.*\nOutput Fluid:\n.*'
        flow = Flow(self.fluid_water, 1)
        flow.out_temperature = 273.15 + 99
        self.assertRegex(str(flow), expected_output, msg='fluid str has not expected pattern')


if __name__ == '__main__':
    unittest.main()
