import sys
import os

# Add the path to your project directory
sys.path.append(os.path.abspath('.'))

import unittest
from src.data_utils import time_to_datetime, celsius_to_kelvin, rse, rmse_6hrs

import unittest
import pandas as pd
from datetime import datetime

class TestTimeToDatetime(unittest.TestCase):

    def test_output_type(self):
        df = pd.DataFrame({'time': [0, 1, 2]})
        result = time_to_datetime(df['time'])
        self.assertIsInstance(result, pd.Series)

    def test_output_values(self):
        df = pd.DataFrame({'time': [0, 1, 2]})
        result = time_to_datetime(df['time'])
        expected = pd.Series(pd.to_datetime(['2018-04-14 00:00:00', '2018-04-14 01:00:00', '2018-04-14 02:00:00']),name="time")
        pd.testing.assert_series_equal(result, expected)

    def test_custom_reference_date(self):
        df = pd.DataFrame({'time': [0, 1, 2]})
        result = time_to_datetime(df['time'], reference_date='2020-01-01')
        expected = pd.Series(pd.to_datetime(['2020-01-01 00:00:00', '2020-01-01 01:00:00', '2020-01-01 02:00:00']),name="time")
        pd.testing.assert_series_equal(result, expected)
    
class TestCelsiusToKelvin(unittest.TestCase):
    def test_celsius_to_kelvin_positive(self):
        self.assertAlmostEqual(celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(celsius_to_kelvin(100), 373.15)
        self.assertAlmostEqual(celsius_to_kelvin(37), 310.15)

    def test_celsius_to_kelvin_negative(self):
        self.assertAlmostEqual(celsius_to_kelvin(-40), 233.15)
        self.assertAlmostEqual(celsius_to_kelvin(-273.15), 0.0)
        self.assertAlmostEqual(celsius_to_kelvin(-100), 173.15)

if __name__ == '__main__':
    unittest.main()
