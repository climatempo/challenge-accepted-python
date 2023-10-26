# data_utils.py
import pandas as pd

def time_to_datetime(time, reference_date='2018-04-14'):
    """
    Convert a dataframe time column to a datetime object.

    Parameters:
    time (pandas.Series): The time column to be converted.

    Returns:
    pandas.Series: The time column converted to a datetime object.

    Example:
    >>> df = pd.DataFrame({'time': [0, 1, 2]})
    """
    time = pd.to_timedelta(time, unit='h')
    return pd.to_datetime(time + pd.to_datetime(reference_date))

def celsius_to_kelvin(temp):
    """
    Convert a temperature in Celsius to Kelvin.

    Parameters:
    temp (float): The temperature in Celsius.

    Returns:
    float: The temperature in Kelvin.

    Example:
    >>> celsius_to_kelvin(0)
    273.15
    """
    return temp + 273.15