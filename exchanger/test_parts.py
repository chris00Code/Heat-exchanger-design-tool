import unittest
from parts import *


class MyTestCase(unittest.TestCase):
    def test_part_init(self):
        part = Part()
        self.assertEqual(part.heat_transferability, 0)

        part = Part(10)
        self.assertEqual(part.heat_transferability, 10)
        self.assertEqual(part.heat_transfer_area, None)
        part = Part(heat_transfer_area=10, heat_transfer_coefficient=5)
        self.assertEqual(part.heat_transferability, 50)
        self.assertEqual(part.heat_transfer_area, 10)

    def test_part_setter(self):
        part = Part(10)
        with self.assertRaises(AttributeError):
            part.heat_transfer_coefficient = 10
        with self.assertRaises(AttributeError):
            part.heat_transfer_area = 10
        part = Part(heat_transfer_area=10, heat_transfer_coefficient=5)
        part.heat_transferability = 10
        print(part)

    def test_part_print(self):
        part = Part(heat_transfer_area=10, heat_transfer_coefficient=5)
        part.hydraulic_diameter = 50
        print(part)

    def test_straightPipe(self):
        pipe = StraightPipe(10, 13)
        self.assertEqual(pipe.heat_transfer_area, None)
        pipe.length = 0.5
        self.assertAlmostEqual(pipe.heat_transfer_area, 17.96, 2)
        pipe.pipe_resistance_coefficient = 5e-2
        print(pipe)

    def test_pipeLayout(self):
        pipe = StraightPipe(10, 13, 1)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout = PipeLayout(pipe, 1)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout.number_pipes = 5
        self.assertEqual(pipe_layout.number_pipes, 5)
        self.assertAlmostEqual(pipe_layout.heat_transfer_area, 35.92 * 5, 1)

    def test_shell(self):
        shell = SquareShell(5, 2, 1)
        print(shell)

    def test_assembly(self):
        shell = SquareShell(5, 2, 1)
        pipe = StraightPipe(10, 13)
        pipe.pipe_resistance_coefficient = 5e-2
        pipe_layout = PipeLayout(pipe)
        assembly = Assembly(shell, pipe_layout)
        assembly.heat_transfer_coefficient = 200
        assembly.pressure_coefficient_shellside = 0.3
        print(assembly)


if __name__ == '__main__':
    unittest.main()
