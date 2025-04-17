import unittest

#create a calculator class with methods for add, subtract, multiply, divide
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    #write test for the Calculator add method
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-2, 3), 1)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subract(5, 3), 2)
        self.assertEqual(self.calc.subract(-5, 3), -8)
        self.assertEqual(self.calc.subract(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(-2, -4), 8)
        self.assertEqual(self.calc.multiply(0, 0), 0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(6, 3), 2)
        self.assertEqual(self.calc.divide(-6, 3), -2)
        self.assertEqual(self.calc.divide(0, 5), 0)
        
        with self.assertRaises(ValueError):
            self.calc.divide(4, 0)


if __name__ == '__main__':
    unittest.main()
