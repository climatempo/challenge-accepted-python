from src.netcdf_utils import read_netcdf_to_dataframe
from src.data_utils import time_to_datetime, celsius_to_kelvin, rse, rmse_6hrs
from src.plot_utils import plot_2_graphs

# Using the read_netcdf_to_dataframe function to the "observation.nc" file
file_name = 'data/observation.nc'
city_coordinates = (8,26)
observed = read_netcdf_to_dataframe(file_name, city_coordinates)
observed["time"] = time_to_datetime(observed["time"])
observed["temperature"] = observed["temperature"].apply(celsius_to_kelvin)
observed["observed"] = observed["temperature"]
observed.drop(columns=["temperature"], inplace=True)

# Using the read_netcdf_to_dataframe function to the "forecast.nc" file
file_name = 'data/forecast.nc'
city_coordinates = (8,26)
predicted = read_netcdf_to_dataframe(file_name, city_coordinates)
predicted["time"] = time_to_datetime(predicted["time"])
predicted["predicted"] = predicted["temperature"]
predicted.drop(columns=["temperature"], inplace=True)

# merge dataframes
df = observed.merge(predicted, on=["time"])
    
# calculate rmse
df["error"] = rse(df,"observed","predicted")

# Calculate rmse for every 6 hours
print(rmse_6hrs(df,"observed","predicted"))

# df.set_index("time", inplace=True)

# Plot the graphs
plot_2_graphs(df)
