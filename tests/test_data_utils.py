import sys
import os
import numpy as np

# Add the path to your project directory
sys.path.append(os.path.abspath('.'))

import unittest
from src.data_utils import time_to_datetime, celsius_to_kelvin, rse, rmse_6hrs
import pandas as pd

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

class TestRSE(unittest.TestCase):

    def test_rse_values(self):
        df = pd.DataFrame({'y': [1, 2, 3, 4, 5],
                           'pred': [1, 3, 2, 2, 4]})
        result = rse(df)
        expected = pd.Series([0., 1., 1., 2., 1.])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)

    def test_rse_with_custom_columns(self):
        df = pd.DataFrame({'obs': [1, 2, 3, 4, 5],
                           'forecast': [1, 3, 2, 2, 4]})
        result = rse(df, y_col="obs", pred_col="forecast")
        expected = pd.Series([0., 1., 1., 2., 1.])
        np.testing.assert_array_almost_equal(result, expected, decimal=2)

class TestRMSE(unittest.TestCase):

    def test_rmse_6hrs(self):
        df = pd.DataFrame({
            "time": pd.date_range('2023-10-25', periods=24, freq='H'),
            "y": np.random.randint(1, 10, 24),
            "pred": np.random.randint(1, 10, 24)
        })
        result = rmse_6hrs(df)
        self.assertIsInstance(result, pd.Series)

    def test_rmse_6hrs_custom_columns(self):
        df = pd.DataFrame({
            "time": pd.date_range('2023-10-25', periods=24, freq='H'),
            "y_values": np.random.randint(1, 10, 24),
            "pred_values": np.random.randint(1, 10, 24)
        })
        result = rmse_6hrs(df, y_col="y_values", pred_col="pred_values")
        self.assertIsInstance(result, pd.Series)

if __name__ == '__main__':
    unittest.main()
