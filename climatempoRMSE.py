#Importing needed Libraries 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import seaborn as sns
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
#%matplotlib inline

#PARAMETERS 
#YOU SHALL CHANGE THOSE AS NEEDED
#_________________________________

path = '' #Folder/Path Where the files are located
path_results = '' #Folder/Path to save results, maps and graphs

#Declare needed variables 
freq_hours = 6  #define time interval in hours

#_________________________________

#FUNCTIONS WE WILL USE

#Declare function to return calculated RMSE for every interval of time
def rmseCalc_list(pred, obse):
    return ((np.nanmean(((np.array(pred) - np.array(obse)) ** 2),
                              axis=0))**0.5)
    
#Define Function to Plot the 2D maps #Unfinished

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

#_________________________________

#Define paths for NetCDF files
path_obs = path+'observation.nc' #Path to observartion file
path_for = path+'forecast.nc' #Path to forecast file

#Define DataFrame Variables and open it with xarray 
df_obs = xr.open_dataset(path_obs)
df_for = xr.open_dataset(path_for)

df_for['t2m'] = df_for['t2m']-273.15 #Normalize Forecast temperature data values, so both DataFrame have temperature in Celsius

#_________________________________

time_start = df_obs.time[0].values #get first datetime from Observation DataFrame
time_stop = df_obs.time[-1].values #get last datetime from Observation DataFrame

# Store equally spaced time points, with given interval as frequency
time_points = pd.date_range(time_start, time_stop, freq=f'{freq_hours}H') #Still needed? 

result_rmse=[] #create empty list to store calculated rmse

#Iterate values in our datasets and for each value call rmseCalc_list function, saving calculated value to result_rmse 
#We are iterating throught a range of 0 to lenght of time_points (wich should be 12 for our dataset)
#Multiplying 'i' by freq_hours to get the data spaced 6 Hours apart.
#Other methods were tested, that one can generalise better for other needs
for i in range(0,len(time_points)):
    i = i*freq_hours
    rmse = rmseCalc_list(df_for['t2m'][i:i+freq_hours],     
                    df_obs['temperatura'][i:i+freq_hours])     
    result_rmse.append(rmse)

rmse_SP =[]

#Loop to iterate results already calculated before and store them on a new variable
for i in range(0,len(result_rmse)):    
    rmse_SP.append(result_rmse[i][8][26])

#Time Series graph for the results stored previously on the variable rmse_SP
plt.plot(rmse_SP, marker='o')
plt.title('São Paulo, Time Series RMSE')
plt.savefig(path_results+'SP_TimeSeriesGraph.png')
plt.show()

#Plot 2D_maps for every value of result_rmse
plotMaps(result_rmse)


##################################################################################
#TO DO:

#Write project.md for github
#Improve Maps, show geographical area with borders. (Cartopy? Basemap? Other?)
#Write NetCDF file with calculated RMSE
#Encapsulate app with Flask?
##################################################################################