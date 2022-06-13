#!/usr/bin/python
# -*- coding: utf-8 -*-

import netCDF4 as nc
import numpy as np
import os

pred_file = os.path.abspath('.') + '/forecast.nc'
obs_file = os.path.abspath('.') + '/observation.nc'

pred_ds = nc.Dataset(pred_file)
obs_ds = nc.Dataset(obs_file)

time = len(pred_ds['time'][:])
lat = len(pred_ds['lat'][:])
lon = len(pred_ds['lon'][:])
interval = int(time / 6)

t2m = np.array(pred_ds['t2m'][:])
temp = np.array(obs_ds['temperatura'][:]) + 273.15

rmse = np.empty((interval, lat, lon))

for i in range(0, lat):

    for j in range(0, lon):

        for k in range(0, interval):

            rmse[k][i][j] = (((t2m[(k*6):((k+1)*6), i, j] - temp[(k*6):((k+1)*6), i, j]) ** 2).sum() / 6) ** 0.5

sao_paulo = rmse[:, 8, 26]
print(sao_paulo)


