# Python Challenge, ClimaTempo

## Python Script to calculate RMSE for given Data, plot 2D-Maps and graphs

Jordon Maule, 29/01/2022

## Features

- Import data from forecast.nc and observation.nc NetCDF files.
- Normalize data units
- Calculate RMSE for entire dataset, with equaly spaced times of 6 hours.
- Plot time series graph for São Paulo RMSE, with equaly spaced times of 6 hours.

## To do

- Improve Maps, show geographical area with borders. (Cartopy? Basemap? Other?)
- Write NetCDF file with calculated RMSE
- Encapsulate app with Flask(?)

## How to use the script

 Before we start, be sure to have the needed libraries installed. If you are using Google Colab or Anaconda Environment, you should already have most of them.
 The packages needed are:  **pandas, matplotlib, numpy, xarray, seaborn, netcdf4** [May be updated when To do list is completed]
 If you need to install any of these libraries please run the following command

```sh
    !pip install LIBRARY_NAME
```

1. Open .py file with a editor, and change the PARAMETERS (files path and time frequency) section to start.
2. Run the script and check the path, configured in Step 1, for the results.

```sh
    python climatempoRMSE.py
```

## How the Script Works
