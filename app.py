#!/usr/bin/python
# -*- coding: utf-8 -*-

import netCDF4 as nc
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

class Challenge():

    def __init__(self, pred_ds, obs_ds):

        self.pred_ds = pred_ds
        self.obs_ds = obs_ds

        self.ntime = len(pred_ds['time'][:])
        self.nlat = len(pred_ds['lat'][:])
        self.nlon = len(pred_ds['lon'][:])
        self.ninterval = int(self.ntime / 6)

        self.t2m = np.array(pred_ds['t2m'][:])
        self.temp = np.array(obs_ds['temperatura'][:]) + 273.15

        self.rmse = np.empty((self.ninterval, self.nlat, self.nlon))

    def calculate_rmse(self):

        for i in range(0, self.nlat):

            for j in range(0, self.nlon):

                for k in range(0, self.ninterval):

                    self.rmse[k][i][j] = (((self.t2m[(k*6):((k+1)*6), i, j] - self.temp[(k*6):((k+1)*6), i, j]) ** 2).sum() / 6) ** 0.5

    def plot(self):

        sao_paulo = self.rmse[:, 8, 26]
        print(sao_paulo)

        # TODO

pred_file = os.path.abspath('.') + '/forecast.nc'
obs_file = os.path.abspath('.') + '/observation.nc'

pred_ds = nc.Dataset(pred_file)
obs_ds = nc.Dataset(obs_file)

ch = Challenge(pred_ds, obs_ds)
ch.calculate_rmse()
ch.plot()

