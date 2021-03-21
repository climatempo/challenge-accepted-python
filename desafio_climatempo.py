## Import of libraries
import pandas as pd
import xarray as xr
import netCDF4 as nc
import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap


## Function list

## add_rmse_2_dataframe
# Calculate the Root Mean Squared Error from forecast and observated temperatures
# input: Panda Dataframe
# output: float value of rmse
def add_rmse_2_dataframe(dataframe):#,a:str='temperatura_forecast',b:str='temperatura'):
    # sqrt((temp_forecast - temp_observation)**2)
    rmse = np.sqrt((((dataframe['temperatura_forecast'] - dataframe['temperatura']) ** 2).mean()))
    return rmse

## define_6_hours_bins
# Split the day in 4 bins with 6 hours each.
# input: Float number x
# Output: Slice of the day
#   0 - 6 AM: 0
#   6 - 12 PM: 1
#  12 - 18 PM: 3
#  18 - 0 AM: 4
def define_6_hours_bins(x):
    return math.floor(x/6)

## create_6_hours_bins_column
# Create three new fields for support calculation and help plot the time series
# input: Panda Dataframe
# Output: Panda Dataframe with three new columns: new_date, new_time, 6_hour_bins
def create_6_hour_bin_column(dataframe):
    dataframe['new_date'] = [d.date() for d in dataframe['time']]
    dataframe['new_time'] = [d.time().hour for d in dataframe['time']]
    dataframe['6_hour_bins'] = dataframe['new_time'].apply(define_6_hours_bins)
    
    return dataframe

## min_distance_2_coordinates
# Calculate the euclidian distance between a given latitude and longitude for each row in the dataset
# input: Pandas Dataframe
#        latitude: Given latitude (default: -23.5489)
#        longitude: Given longitude (default: -46.6388)
def min_distance_2_coordinate(dataframe, latitude = -23.5489, longitude = -46.6388):
    distance = math.sqrt((dataframe.lat - latitude) **2 + (dataframe.lon - longitude)**2)
    return distance

# Prepare the data to be analised, also convert netCDF4 file to Dataframe
nc1 = xr.open_dataset('forecast.nc').to_dataframe().reset_index()
# renaming column to match clumns labels in each dataset
rename_columns = {'t2m':'temperatura'}
nc1.rename(columns=rename_columns, inplace=True)
# Convert K to Celsius
nc1['temperatura']=nc1['temperatura'] - 273.15

nc2 = xr.open_dataset('observation.nc').to_dataframe().reset_index()
#

#Anchor point to check a newly created dataframe based on forecast data
nc1.describe()

#Anchor point to check a newly created dataframe based on observation data
nc2.describe()

# Analysing the both dataframes, nc1 has same number of data for all columns, but nc2 has some missing values. ALso, the number of
# errors is minimal (144 in 66599), so I decide to remove these data. Also both datasets have similar mean and quartiles

#Analising data for invalid/absent data and removing invalid data.
nc2.loc[nc2['temperatura'].isnull()]
nc2.dropna(inplace=True)

# Check if data was deleted
nc2.loc[nc2['temperatura'].isnull()]

# Adding the support columns to dataframe
nc1 = create_6_hour_bin_column(nc1)
nc2= create_6_hour_bin_column(nc2)

# Latitude and Longitude coordinates are similar in both datasets, so I decide merge only the
# forecast temperature column to observation dataframe. Both dataset has the same column label temperature
# so, I renamed forecast temperature adding a suffix _forecast to differ both.
forecast_df = nc2.merge(nc1['temperatura'], left_index=True, right_index=True, suffixes=['','_forecast'])
    
# For time series, usually you need to group similar data (in this case we are looking for plot temperatures in 4 slices
# of the day in a unique latitude and longitude), so I merge latitude, longitude, date and part of the day to help me plot the data. 
# Also, I add the RMSE calculations for each row in the dataframe
final_df = forecast_df.groupby(['lat', 'lon', 'new_date', '6_hour_bins']).apply(lambda x: add_rmse_2_dataframe(x)).to_frame('rmse').reset_index()

# We are looking for a specific coordinate (lat: -23.5489 / lon: -46.6388) and we need to find the nearly coordinate in the dataset
# for this I use the euclidian distances calculated in each row os dataset
final_df['distance'] = final_df.apply(min_distance_2_coordinate, axis=1)

# Formatting date to plot 
final_df['new_date'] = (final_df['new_date'].apply(pd.to_datetime) + final_df['6_hour_bins'].apply(lambda x: pd.Timedelta(f'{6*x} h')))

# Exchange numeric index to newly created date format
final_df.index = final_df['new_date']

# Plotting the RMSE index to each period of the time series
for date in final_df.new_date.unique():
    # Checking if the row is part of the period
    mask = final_df['new_date'] == date
    
    # assigning points to axis
    y = final_df.loc[mask,'lat'].values
    x = final_df.loc[mask,'lon'].values
    
    # Filling plot with triangules (should have a better resolution than normal meshgrid function)
    grid = mpl.tri.Triangulation(x, y)
    
    # Plotting RMSE index
    z = final_df.loc[date,'rmse'].values
    figure, ax = plt.subplots(figsize = (20,5))
    ax.set_aspect('equal')
    countour = ax.tricontourf(grid, z)
    figure.colorbar(countour)
    ax.tricontour(grid, z)
    ax.set_title('RMSE - {0}'.format(pd.to_datetime(date).strftime("%d/%m/%Y  %H:%M:%S")))
    # Plot the map
    plt.show()

# Find the nearest coordinate to the given coordinates in the dataset
latitude_longitude_dictionary = final_df.sort_values('distance').iloc[0][['lat','lon']].to_dict()

# Create a new dataframe just for the given coordinates
final_df_sp = final_df.query('lat == {lat} and lon == {lon}'.format(**latitude_longitude_dictionary))

# Plot time series of final_df_sp dataframe using
fig, ax = plt.subplots(figsize=(20,9))
ax.set_title('lat: -23.5489 / lon: -46.6388 Timeseries RMSE from 14/04/2018 to 16/04/2018', fontdict = {'size':22});
plt.plot(final_df_sp.new_date,final_df_sp.rmse,'-o',lw = 2)

date_format = mpl.dates.DateFormatter('%d/%m/%Y')
ax.xaxis.set_major_formatter(date_format)

plt.savefig("lat:-23.5489_lon:-46.6388_timeseries_14_to_16_04_2018.png")

#plt.show()

final_netcdf = xr.Dataset.from_dataframe(final_df, sparse=False)
final_netcdf.to_netcdf('forecast_observation_rmse.nc')
