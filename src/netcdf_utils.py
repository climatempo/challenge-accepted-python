# netcdf_utils.py

import netCDF4 as nc
import pandas as pd
import os


def read_netcdf_to_dataframe(file_name, city_coordinates, temp_key = None, lines=None):
    """
    Read data from a NetCDF file and convert it into a pandas DataFrame.
    Data is either observed or forecasted temperature data.
    Temperature column in observed data is stored in "temperatura"
    Temperature column in forecasted data is stored in "t2m"

    Parameters:
    file_name (str): The path to the NetCDF file.
    lines (int or None, optional): The number of lines to read from the NetCDF file. If None, all lines will be read.
    city_coordinates (tuple): The latitude and longitude of the city to be read from the NetCDF file.
    temp_key (str): The name of the temperature column in the NetCDF file.

    Returns:
    pandas.DataFrame: A pandas DataFrame containing the data from the NetCDF file.

    Raises:
    FileNotFoundError: If the specified file_path does not exist.
    KeyError: If the temperature column name or 'time' is not present in the NetCDF file.

    Example:
    >>> df = read_netcdf_to_dataframe('example.nc', (lat, lon))
    """
    # Open file
    data = nc.Dataset(file_name, "r", format = "NETCDF4")

    # Get column names
    variable_names = list(data.variables.keys())

    # Get temperature column name
    if temp_key is None:
        if 'temperatura' in variable_names:
            temperature_column_name = 'temperatura'
        elif 't2m' in variable_names:
            temperature_column_name = 't2m'

    # Check if temperature_column_name is in the file
    if temperature_column_name not in variable_names:
        raise KeyError("The column name is not present in the NetCDF file.")
    
    # Check if time is in the file
    if 'time' not in variable_names:
        raise KeyError("Time is not present in the NetCDF file.")
    
    # Create a dictionary to store the data
    data_dict = {}

    # Get the time data
    data_dict["time"] = data.variables["time"][:].data[:]
    if lines is not None:
        data_dict["time"] = data_dict["time"][:lines]

    # Get the temperature data
    data_dict['temperature'] = []
    for i in range(len(data_dict["time"])):
        data_dict['temperature'].append(data.variables[temperature_column_name][i].data[city_coordinates[0],city_coordinates[1]])
        if lines is not None and i == lines-1:
            break

    # Close file
    data.close()

    # return DataFrame
    df = pd.DataFrame(data_dict)
    return df

def write_dataframe_to_netcdf(df, file_path):
    """
    Write a pandas DataFrame to a NetCDF file.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be written to the NetCDF file.
    file_path (str): The path to the output NetCDF file.

    Returns:
    None

    Raises:
    TypeError: If the input 'df' is not a pandas DataFrame.
    IOError: If the file_path is invalid or inaccessible.
    FileExistsError: If the file name already exists.

    Example:
    >>> data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    >>> df = pd.DataFrame(data)
    >>> write_dataframe_to_netcdf(df, 'output.nc')
    """

    if os.path.exists(file_path):
        raise FileExistsError("The file name is already used.")

    dataset = None
    try:
        dataset = nc.Dataset(file_path, 'w', format='NETCDF4')

        for col in df.columns:
            dataset.createDimension(col, df[col].shape[0])

        for col in df.columns:
            var = dataset.createVariable(col, df[col].dtype, (col,))
            var[:] = df[col].values

    except IOError as e:
        raise e
    finally:
        if dataset is not None:
            dataset.close()

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

if __name__ == '__main__':
    # Example usage
    data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]} # Create a sample DataFrame
    df = pd.DataFrame(data)
    file_name = 'test.nc'
    write_dataframe_to_netcdf(df, file_name) # Write the DataFrame to a NetCDF file
    # Deleting the file 'test.nc'
    if os.path.exists(file_name):
        os.remove(file_name)
    
    # Using the read_netcdf_to_dataframe function to the "observation.nc" file
    file_name = 'data/observation.nc'
    city_coordinates = (8,26)
    df = read_netcdf_to_dataframe(file_name, city_coordinates)
    print(df.head())

    # Using the read_netcdf_to_dataframe function to the "forecast.nc" file
    file_name = 'data/forecast.nc'
    city_coordinates = (8,26)
    df = read_netcdf_to_dataframe(file_name, city_coordinates)
    print(df.head())
    df["time"] = time_to_datetime(df["time"])
    print(df.head())