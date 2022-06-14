#!/usr/bin/python
# -*- coding: utf-8 -*-

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
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
        self.lat = np.array(pred_ds['lat'][:])
        self.lon = np.array(pred_ds['lon'][:])

        self.rmse = np.empty((self.ninterval, self.nlat, self.nlon))

    def calculate_rmse(self):

        for i in range(0, self.nlat):

            for j in range(0, self.nlon):

                for k in range(0, self.ninterval):

                    self.rmse[k][i][j] = (((self.t2m[(k*6):((k+1)*6), i, j] - self.temp[(k*6):((k+1)*6), i, j]) ** 2).sum() / 6) ** 0.5

    def plot(self):

        fig, ax = plt.subplots()

        # Gráfico RMSE para São Paulo

        sao_paulo = self.rmse[:, 8, 26]
        interval = np.array([i for i in range(0, self.ninterval)]) + 1

        ax.plot(interval, sao_paulo)
        ax.set_title('Série Temporal - RMSE São Paulo')
        ax.set_xlabel('Período')
        ax.set_ylabel('RMSE')

        # Mapas

        y = np.array([self.lat[8]])
        x = np.array([self.lon[26]])
        period1 = np.array([self.rmse[0, 8, 26]]) * 50
        period2 = np.array([self.rmse[1, 8, 26]]) * 50
        period3 = np.array([self.rmse[2, 8, 26]]) * 50
        period4 = np.array([self.rmse[3, 8, 26]]) * 50
        period5 = np.array([self.rmse[4, 8, 26]]) * 50
        period6 = np.array([self.rmse[5, 8, 26]]) * 50
        period7 = np.array([self.rmse[6, 8, 26]]) * 50
        period8 = np.array([self.rmse[7, 8, 26]]) * 50
        period9 = np.array([self.rmse[8, 8, 26]]) * 50
        period10 = np.array([self.rmse[9, 8, 26]]) * 50
        period11 = np.array([self.rmse[10, 8, 26]]) * 50
        period12 = np.array([self.rmse[11, 8, 26]]) * 50

        map_file = os.path.abspath('.') + '/gadm36_BRA_0.shx'
        brasil_map = gpd.read_file(map_file)

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period1)
        ax.set_title('RMSE São Paulo - Período 1')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period2)
        ax.set_title('RMSE São Paulo - Período 2')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period3)
        ax.set_title('RMSE São Paulo - Período 3')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period4)
        ax.set_title('RMSE São Paulo - Período 4')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period5)
        ax.set_title('RMSE São Paulo - Período 5')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period6)
        ax.set_title('RMSE São Paulo - Período 6')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period7)
        ax.set_title('RMSE São Paulo - Período 7')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period8)
        ax.set_title('RMSE São Paulo - Período 8')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period9)
        ax.set_title('RMSE São Paulo - Período 9')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period10)
        ax.set_title('RMSE São Paulo - Período 10')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period11)
        ax.set_title('RMSE São Paulo - Período 11')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        fig, ax = plt.subplots()
        brasil_map.plot(ax=ax)
        ax.scatter(x, y, c='#000000', s=period12)
        ax.set_title('RMSE São Paulo - Período 12')
        ax.set_xlabel('Longetude')
        ax.set_ylabel('Latitude')

        plt.show()

if __name__ == '__main__':

    pred_file = os.path.abspath('.') + '/forecast.nc'
    obs_file = os.path.abspath('.') + '/observation.nc'

    pred_ds = nc.Dataset(pred_file)
    obs_ds = nc.Dataset(obs_file)

    ch = Challenge(pred_ds, obs_ds)
    ch.calculate_rmse()
    ch.plot()

