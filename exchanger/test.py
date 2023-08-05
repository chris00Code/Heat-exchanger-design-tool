import unittest

import pyfluids


class FluidTests(unittest.TestCase):
    from pyfluids import Fluid as fldFluid
    from pyfluids import Mixture as fldMixture
    from stream import Fluid

    def test_fluid_init(self):
        with self.assertRaises(TypeError):
            fluid = self.Fluid()
        fluid = self.Fluid("Water")
        self.assertEqual(fluid.title, "Water")

        self.assertEqual(fluid.fluid.units_system, pyfluids.UnitsSystem.SI)

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


    def test_something(self):
        fluid = self.Fluid("Water")
        print(fluid.fluid.enthalpy)
        new_fluid = fluid.fluid.heating_to_enthalpy(90000)
        print(fluid)
        n = self.Fluid(new_fluid)
        print(n)
        n2 = n.clone()
        print(n2)

if __name__ == '__main__':
    unittest.main()
