import unittest
from parts import *


class PartTests(unittest.TestCase):
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
        pipe.heat_transfer_coefficient = 200
        print(pipe)

    def test_pipeLayout(self):
        pipe = StraightPipe(10, 13, 1)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout = PipeLayout(pipe, 1)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout.number_pipes = 5
        self.assertEqual(pipe_layout.number_pipes, 5)
        self.assertAlmostEqual(pipe_layout.heat_transfer_area, 35.92 * 5, 1)
        pipe.heat_transfer_coefficient = 200
        self.assertAlmostEqual(pipe.heat_transferability, 7184.49, 1)
        self.assertAlmostEqual(pipe_layout.heat_transferability, 7184.49*5, 1)
        #print(pipe_layout)


    def test_shellGeometry(self):
        shell = SquareShellGeometry(5, 2, 1)
        print(shell)

    def test_assembly(self):
        shell = SquareShellGeometry(5, 2, 1)
        pipe = StraightPipe(10e-3, 13e-3)
        pipe.pipe_resistance_coefficient = 5e-2
        pipe_layout = PipeLayout(pipe, 5)
        assembly = Assembly(shell, pipe_layout)
        assembly.heat_transfer_coefficient = 200
        assembly.pressure_coefficient_shellside = 0.3
        print(assembly)

    def test_assembly_squaredShel(self):
        shell = SquareShellGeometry(1, 0.35, 0.18)
        pipe = StraightPipe(8e-3, 12e-3, 3.233)
        pipe_layout = PipeLayout(pipe, 20)
        assembly = Assembly(shell, pipe_layout)
        print(assembly)

    def test_assembly_baffles(self):
        shell = SquareShellGeometry(5, 2, 1)
        pipe = StraightPipe(10e-3, 13e-3)
        pipe_layout = PipeLayout(pipe, 5)
        baffle = SegmentalBaffle(1, 50)
        print(baffle)
        assembly = Assembly(shell, pipe_layout, baffle)
        print(assembly)

    def test_assembly_floworder(self):
        shell = SquareShellGeometry(5, 2, 1)
        pipe = StraightPipe(10e-3, 13e-3)
        pipe_layout = PipeLayout(pipe, 5)
        inlets = Inlets('ul','dl')
        assembly = Assembly(shell, pipe_layout, inlets=inlets)
        print(assembly)

if __name__ == '__main__':
    unittest.main()
