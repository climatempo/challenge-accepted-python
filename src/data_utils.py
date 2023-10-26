# data_utils.py
import pandas as pd
import numpy as np

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

def rse(df, y_col = "y", pred_col = "pred"):
    """
    Calculate the root squared error for every row in a dataframe.

    Parameters:
    df (pandas.DataFrame): Dataframe with columns y and pred.

    Returns:
    pandas.Series: Absolute error for every row in the dataframe.
    """
    return np.abs(df[y_col] - df[pred_col])

def rmse_6hrs(df, y_col = "y", pred_col = "pred"):
    """
    Calculate the root mean squared error for every 6 hours in a dataframe.

    Parameters:
    df (pandas.DataFrame): Dataframe with columns y and pred.

    Returns:
    pandas.Series: Root mean squared error for every 6 hours in the dataframe.
    """
    df["error"] = rse(df, y_col, pred_col)
    df.set_index("time", inplace=True)
    return df["error"].resample("6H").mean()

if __name__ == "__main__":
    from netcdf_utils import read_netcdf_to_dataframe
    file_name = 'data/observation.nc'
    city_coordinates = (8,26)
    observed = read_netcdf_to_dataframe(file_name, city_coordinates)
    observed["time"] = time_to_datetime(observed["time"])
    observed["temperature"] = observed["temperature"].apply(celsius_to_kelvin)
    observed["observed"] = observed["temperature"]
    observed.drop(columns=["temperature"], inplace=True)
    print(observed.head())

    # Using the read_netcdf_to_dataframe function to the "forecast.nc" file
    file_name = 'data/forecast.nc'
    city_coordinates = (8,26)
    predicted = read_netcdf_to_dataframe(file_name, city_coordinates)
    predicted["time"] = time_to_datetime(predicted["time"])
    predicted["predicted"] = predicted["temperature"]
    predicted.drop(columns=["temperature"], inplace=True)
    print(predicted.head())

    # merge dataframes
    df = observed.merge(predicted, on=["time"])
    
    # calculate rmse
    df["error"] = rse(df,"observed","predicted")
    print(df.head())
    print(rmse_6hrs(df,"observed","predicted"))