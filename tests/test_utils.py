import unittest
from exchanger.utils import get_available_class_names


class TestUtils(unittest.TestCase):
    def test_available_classes(self):
        self.assertListEqual(get_available_class_names(unittest), [])
        self.assertIn('SkipTest', get_available_class_names(unittest.case))
        self.assertIn('SkipTest', get_available_class_names(unittest.case, Exception))


if __name__ == '__main__':
    unittest.main()
