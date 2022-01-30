# Python Challenge, ClimaTempo

## Python Script to calculate RMSE for given Data, plot 2D-Maps and graphs

Jordon Maule, 29/01/2022

## Features

- Import data from forecast.nc and observation.nc NetCDF files.
- Normalize data units
- Calculate RMSE for entire dataset, with equaly spaced times of 6 hours.
- Plot time series graph for São Paulo RMSE, with equaly spaced times of 6 hours.
- Plot 2D-Maps of geographical area, with a heatmap overlay of calculated RMSE.

## To do

- Write NetCDF file with calculated RMSE
- Encapsulate app with Flask(?)

## How to use the script

 Before we start, be sure to have the needed libraries installed. If you are using Google Colab or Anaconda Environment, you should already have most of them.
 The packages needed are:  **pandas, matplotlib, numpy, xarray, netcdf4, cartopy**
 If you need to install any of these libraries please run the following command

```sh
    pip install LIBRARY_NAME
```

1. Open .py file with an editor, and change the PARAMETERS (files path and time frequency) section to start.
2. Run the script and check the path, configured in Step 1, for the results.

```sh
    python climatempoRMSE.py
```

## How the Script Works

1. Importing the needed libraries:

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
```

2. Declare some variables that will help the code generalize better. (For now we are able to easily change time intervals and path of data and results)
Be sure to configure 'freq_hours' in HOURS.

```python
path = '%PATH'
path_results = '%PATH'
freq_hours = %TIME_INTERVAL
```

3. Declare the functions that will be used to calculate RMSE and plot 2D Maps.

Function 'rmse_Calc_list(pred, obse)', needs two arguments, one for the predicted/forecast data and one for the observed/actual data.
We are using 'np.array()' to convert the data so we are able to use 'np.nanmean()', as the original data is stored in a xarray object and can't be passed to 'np.nanmean()' as it is. 'np.nanmean()' is used to calculate the means, ignoring NaNs. #This method can be changed if we pre-process the data to deal with NaNs.

```python
def rmseCalc_list(pred, obse):
    return ((np.nanmean(((np.array(pred) - np.array(obse)) ** 2),
                              axis=0))**0.5)
```

Function 'plotMaps(given_list)' . #Markdown unfinshed, modified after adding cartopy.

```python
def plotMaps(given_list): 

  lats = df_obs['lat'][:]
  lons = df_obs['lon'][:]

  for i in range(0, len(time_points)):
    ax = plt.axes(projection=ccrs.PlateCarree())

    plt.contourf(lons, lats, given_list[i], 60,
             transform=ccrs.PlateCarree(), cmap="coolwarm")
    
    
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')
    
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(states_provinces, edgecolor='black')

    ax.coastlines()
    
    plt.title(time_points[i])
    plt.savefig(path_results+f'{i}_2D_mapRMSE.png')      
    plt.show()
```

4. Define variables with the NetCDF files path, name for the file is hardcoded.

```python
path_obs = path+'observation.nc'
path_for = path+'forecast.nc'
```

Define DataFrame Variables and open it with xarray.

```python
df_obs = xr.open_dataset(path_obs)
df_for = xr.open_dataset(path_for)
```

5. Normalize Forecast temperature data values, so both DataFrames have temperature in Celsius

```python

df_for['t2m'] = df_for['t2m']-273.15

```

6. Get First and last datetime values from observation DataFrame

```python
time_start = df_obs.time[0].values
time_stop = df_obs.time[-1].values
```

Store equally spaced time points, with given time interval as frequency

```python
time_points = pd.date_range(time_start, time_stop, freq=f'{freq_hours}H') 
```

7. Create empty list to store calculated rmse.
Iterate values in our dataframes and for each value call 'rmseCalc_list' function, saving calculated value to a list variable 'result_rmse'.
We are iterating thought a range of 0 to 'lenght of time_points' (wich should be 12 for our data)
Multiplying 'i' by 'freq_hours' to get the data spaced equally by the interval previously configured.

```python
result_rmse=[] 

for i in range(0,len(time_points)):
    i = i*freq_hours
    rmse = rmseCalc_list(df_for['t2m'][i:i+freq_hours],     
                    df_obs['temperatura'][i:i+freq_hours])     
    result_rmse.append(rmse)
```

8. Create empty list to store calculated rmse for São Paulo only.
Loop to iterate results already calculated in the previous step and store them on a new variable.

```python
rmse_SP =[]

for i in range(0,len(result_rmse)):    
    rmse_SP.append(result_rmse[i][8][26])
```

9. Time Series graph for the results stored previously on the variable rmse_SP

```python
plt.plot(rmse_SP, marker='o')
plt.title('São Paulo, Time Series RMSE')
plt.savefig(path_results+'SP_TimeSeriesGraph.png')
plt.show()
```

10. Call function 'plotMaps()' with the list with calculated RMSE results as argument.

```python
plotMaps(result_rmse)
```

11. To Do, save RMSE calculated results to .nc file.

```python
# To Do, save RMSE calculated results to .nc file. 

```