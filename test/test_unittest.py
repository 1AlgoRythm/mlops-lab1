import sys
import os
import unittest

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import calculator


class TestCalculator(unittest.TestCase):

    def test_fun1(self):
        self.assertEqual(calculator.fun1(2, 3), 5)
        self.assertEqual(calculator.fun1(5, 0), 5)
        
        self.assertEqual(calculator.fun1(-1, 1), 0)
        self.assertEqual(calculator.fun1(-1, -1), -2)

    def test_fun2(self):
        self.assertEqual(calculator.fun2(2, 3), -1)
        self.assertEqual(calculator.fun2(5, 0), 5)
        self.assertEqual(calculator.fun2(-1, 1), -2)
        self.assertEqual(calculator.fun2(-1, -1), 0)

    def test_fun3(self):
        self.assertEqual(calculator.fun3(2, 3), 6)
        self.assertEqual(calculator.fun3(5, 0), 0)
        self.assertEqual(calculator.fun3(-1, 1), -1)
        self.assertEqual(calculator.fun3(-1, -1), 1)

    def test_fun4(self):
        self.assertEqual(calculator.fun4(2, 3, 5), 10)
        self.assertEqual(calculator.fun4(5, 0, -1), 4)
        self.assertEqual(calculator.fun4(-1, -1, -1), -3)
        self.assertEqual(calculator.fun4(-1, -1, 100), 98)
    
    def test_fun4_with_floats(self):
        self.assertEqual(calculator.fun4(1.5, 2.5, 1), 5.0)

    def test_float_addition_needs_tolerance(self):
        # 0.1 + 0.2 is 0.30000000000000004, so compare to a few decimal places
        self.assertAlmostEqual(calculator.fun1(0.1, 0.2), 0.3)

    def test_fun4_rejects_non_numbers(self):
        with self.assertRaises(ValueError):
            calculator.fun4("a", 2, 3)
        with self.assertRaises(ValueError):
            calculator.fun4(1, "b", 3)
        with self.assertRaises(ValueError):
            calculator.fun4(1, 2, "c")

    def test_fun1_fun2_fun3_reject_non_numbers(self):
        with self.assertRaises(ValueError):
            calculator.fun1("2", 3)
        with self.assertRaises(ValueError):
            calculator.fun2(1, None)
        with self.assertRaises(ValueError):
            calculator.fun3(1, [2])




if __name__ == '__main__':
    unittest.main()