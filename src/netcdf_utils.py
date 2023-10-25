# netcdf_utils.py
import netCDF4 as nc
import pandas as pd

def read_netcdf_to_dataframe(file_path, lines=None):
    """
    Read data from a NetCDF file and convert it into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the NetCDF file.
    lines (int or None, optional): The number of lines to read from the NetCDF file. If None, all lines will be read.

    Returns:
    pandas.DataFrame: A pandas DataFrame containing the data from the NetCDF file.

    Raises:
    FileNotFoundError: If the specified file_path does not exist.
    KeyError: If 'variable_name' is not present in the NetCDF file.

    Example:
    >>> df = read_netcdf_to_dataframe('example.nc', lines=100)
    """

    data = nc.Dataset(file_path, mode='r')

    if lines is not None:
        df = pd.DataFrame(data.variables['variable_name'][:lines])
    else:
        df = pd.DataFrame(data.variables['variable_name'][:])

    data.close()
    return df