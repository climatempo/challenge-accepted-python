# netcdf_utils.py

import netCDF4 as nc
import pandas as pd
import os

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

    # Getting all variable names
    variable_names = list(data.variables.keys())

    data_dict = {}

    if lines is not None:
        for var_name in variable_names:
            data_dict[var_name] = data.variables[var_name][:lines]
    else:
        for var_name in variable_names:
            data_dict[var_name] = data.variables[var_name][:]

    data.close()
    return pd.DataFrame(data_dict)



def write_dataframe_to_netcdf(df, file_path, variable_name='variable_name'):
    """
    Write a pandas DataFrame to a NetCDF file.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be written to the NetCDF file.
    file_path (str): The path to the output NetCDF file.
    variable_name (str, optional): The name of the NetCDF variable. Default is 'variable_name'.

    Returns:
    None

    Raises:
    TypeError: If the input 'df' is not a pandas DataFrame.
    IOError: If the file_path is invalid or inaccessible.
    FileExistsError: If the file name already exists.

    Example:
    >>> data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    >>> df = pd.DataFrame(data)
    >>> write_dataframe_to_netcdf(df, 'output.nc', variable_name='my_variable')
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


if __name__ == '__main__':
    # Example usage
    data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]} # Create a sample DataFrame
    df = pd.DataFrame(data)
    file_name = 'test.nc'
    write_dataframe_to_netcdf(df, file_name, variable_name='my_variable') # Write the DataFrame to a NetCDF file

    df1 = read_netcdf_to_dataframe(file_name, lines=100) # Read the NetCDF file into a DataFrame

    print(df) # Check if the DataFrames are equal
    print(df1)

    # Deleting the file 'test.nc'
    if os.path.exists(file_name):
        os.remove(file_name)