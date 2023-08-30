import unittest
from exchanger.parts import *


class TestParts(unittest.TestCase):

    def test_heat_parameter_setter(self):
        part = Part()
        self.assertEqual(part.heat_transferability, NotImplemented)
        self.assertEqual(part.heat_transfer_coefficient, NotImplemented)
        self.assertEqual(part.heat_transfer_area, NotImplemented)

        part = Part(heat_transfer_area=10)
        self.assertEqual(part.heat_transferability, NotImplemented)
        self.assertEqual(part.heat_transfer_coefficient, NotImplemented)
        self.assertEqual(part.heat_transfer_area, 10)

        part = Part(heat_transfer_coefficient=10)
        self.assertEqual(part.heat_transferability, NotImplemented)
        self.assertEqual(part.heat_transfer_coefficient, 10)
        self.assertEqual(part.heat_transfer_area, NotImplemented)

        part = Part(heat_transferability=10)
        self.assertEqual(part.heat_transferability, 10)
        self.assertEqual(part.heat_transfer_coefficient, NotImplemented)
        self.assertEqual(part.heat_transfer_area, NotImplemented)

        part = Part(heat_transfer_area=10, heat_transfer_coefficient=50)
        self.assertEqual(part.heat_transferability, 500)
        self.assertEqual(part.heat_transfer_coefficient, 50)
        self.assertEqual(part.heat_transfer_area, 10)

        part = Part(heat_transfer_area=10, heat_transfer_coefficient=50, heat_transferability=500)
        self.assertEqual(part.heat_transferability, 500)
        self.assertEqual(part.heat_transfer_coefficient, 50)
        self.assertEqual(part.heat_transfer_area, 10)

        part = Part(heat_transfer_area=10, heat_transfer_coefficient=50, heat_transferability=500)
        with self.assertWarnsRegex(Warning,
                                   'heat transfer parameters not consistent$',
                                   msg='no warning when setting not consistent heat parameters'):
            part.heat_transferability = 250
        with self.assertWarnsRegex(Warning,
                                   'heat transfer parameters are not consistent, '
                                   'defined parameter will be returned \(not calculated one\)',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertEqual(part.heat_transferability, 250)
        with self.assertWarnsRegex(Warning,
                                   'heat transfer parameters are not consistent, '
                                   'defined parameter will be returned \(not calculated one\)',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertEqual(part.heat_transfer_coefficient, 50)
        with self.assertWarnsRegex(Warning,
                                   'heat transfer parameters are not consistent, '
                                   'defined parameter will be returned \(not calculated one\)',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertEqual(part.heat_transfer_area, 10)

    def test_part_print(self):
        part = Part(heat_transfer_area=10, heat_transfer_coefficient=5)
        part.hydraulic_diameter = 50
        print(part)

    def test_pipe_kwargs(self):
        pipe = Pipe(10, diameter_out=13, heat_transfer_coefficient=200)
        self.assertEqual(pipe.diameter_in, 10)
        self.assertEqual(pipe.diameter_out, 13)
        self.assertEqual(pipe.heat_transfer_coefficient, 200)

        pipe = Pipe(10, diameter_out=13, length=1, heat_transfer_coefficient=200)
        self.assertEqual(pipe.diameter_in, 10)
        self.assertEqual(pipe.diameter_out, 13)
        self.assertEqual(pipe.heat_transfer_coefficient, 200)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 1)
        self.assertAlmostEqual(pipe.heat_transferability, 7184.49, 1)

        pipe = Pipe(10, diameter_out=13, length=1, heat_transfer_coefficient=200, heat_transferability=500)
        with self.assertWarnsRegex(Warning,
                                   'function not available, value is not set',
                                   msg='setting heat transfer area should not be possible'):
            pipe.heat_transfer_area = 500

        self.assertEqual(pipe.diameter_in, 10)
        self.assertEqual(pipe.diameter_out, 13)
        self.assertEqual(pipe.heat_transfer_coefficient, 200)
        with self.assertWarnsRegex(Warning,
                                   'heat transfer parameters are not consistent, '
                                   'defined parameter will be returned \(not calculated one\)',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 1)
        with self.assertWarnsRegex(Warning,
                                   'heat transfer parameters are not consistent, '
                                   'defined parameter will be returned \(not calculated one\)',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertEqual(pipe.heat_transferability, 500)

    def test_straightPipe(self):
        pipe = StraightPipe(10, 13)
        self.assertEqual(pipe.heat_transfer_area, NotImplemented)
        pipe.length = 0.5
        self.assertAlmostEqual(pipe.heat_transfer_area, 17.96, 2)
        pipe.pipe_resistance_coefficient = 5e-2
        pipe.heat_transfer_coefficient = 200
        self.assertAlmostEqual(pipe.heat_transferability, 3592.249, 2)

    def test_pipe_layout_heat_parameters(self):
        pipe = StraightPipe(10, 13, 1, heat_transfer_coefficient=200)
        pipe_layout = PipeLayout(pipe, 5)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout.heat_transfer_area = 500
        with self.assertWarnsRegex(Warning,
                                   'defined value is not calculated, defined is returned',
                                   msg='no warning when heat parameters are not consistent'):
            self.assertEqual(pipe_layout.heat_transfer_area, 500)
        pipe_layout.heat_transfer_coefficient = 200
        self.assertEqual(pipe_layout.heat_transfer_coefficient, 200)

    def test_pipeLayout(self):
        pipe = StraightPipe(10, 13, 1, heat_transfer_coefficient=200)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout = PipeLayout(pipe, 1)
        self.assertAlmostEqual(pipe.heat_transfer_area, 35.92, 2)
        pipe_layout.number_pipes = 5
        self.assertEqual(pipe_layout.number_pipes, 5)
        self.assertAlmostEqual(pipe_layout.heat_transfer_area, 35.92 * 5, 1)
        pipe.heat_transfer_coefficient = 200
        self.assertAlmostEqual(pipe.heat_transferability, 7184.49, 1)
        self.assertAlmostEqual(pipe_layout.heat_transferability, 7184.49 * 5, 1)


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
        inlets = Inlets('ul', 'dl')
        assembly = Assembly(shell, pipe_layout, inlets=inlets)
        print(assembly)


if __name__ == '__main__':
    unittest.main()
