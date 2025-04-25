import unittest
from datetime import datetime

# Create a Constraints class with functions for symbol, chart_type, time_series, start_date, and end_date
class Constraints:
    def symbol(self, a):
        return a.isalpha() and a.isupper() and 1 <= len(a) <= 7

    def chart_type(self, a):
        return a in ['1', '2']

    def time_series(self, a):
        return a in ['1', '2', '3', '4']

    def start_date(self, a):
        try:
            datetime.strptime(a, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def end_date(self, a, b):
        try:
            return datetime.strptime(b, '%Y-%m-%d') >= datetime.strptime(a, '%Y-%m-%d')
        except ValueError:
            return False


class TestConstraints(unittest.TestCase):
    def setUp(self):
        self.const = Constraints()

    #write test for the Contstraint symbol method
    def test_symbol(self):
        self.assertTrue(self.const.symbol("MMM"))
        self.assertFalse(self.const.symbol("amt"))        
        self.assertFalse(self.const.symbol("SCG123"))     
        self.assertFalse(self.const.symbol("TOOLONGG"))   
        self.assertFalse(self.const.symbol(""))           

    def test_chart_type(self):
        self.assertTrue(self.const.chart_type("1"))
        self.assertTrue(self.const.chart_type("2"))
        self.assertFalse(self.const.chart_type("3"))
        self.assertFalse(self.const.chart_type("bar"))

    def test_time_series(self):
        self.assertTrue(self.const.time_series("1"))
        self.assertTrue(self.const.time_series("2"))
        self.assertTrue(self.const.time_series("3"))
        self.assertTrue(self.const.time_series("4"))
        self.assertFalse(self.const.time_series("5"))
        self.assertFalse(self.const.time_series("weekly"))

    def test_start_date(self):
        self.assertTrue(self.const.start_date("2022-11-06"))
        self.assertFalse(self.const.start_date("11-06-2022"))
        self.assertFalse(self.const.start_date("November 6, 2022"))
        self.assertFalse(self.const.start_date(""))

    def test_end_date(self):
        self.assertTrue(self.const.end_date("2022-01-01", "2022-01-02"))
        self.assertTrue(self.const.end_date("2022-01-01", "2022-01-01"))
        self.assertFalse(self.const.end_date("2022-01-02", "2022-01-01"))
        self.assertFalse(self.const.end_date("2022-01-01", "date"))

if __name__ == '__main__':
    unittest.main()