import matplotlib.pyplot as plt 
import aux
from netCDF4 import Dataset
import numpy as np
import glob as gl
import os

# LISTANDO O CAMINHO PARA OS ARQUIVOS
filenames = gl.glob(os.getcwd()+'/*.nc')

# LENDO OS ARQUIVOS NETCDF
forecast    = Dataset(filenames[0], 'r')
observation = Dataset(filenames[1], 'r')

# EXTRAINDO AS VARIÁVEIS DOS ARQUIVOS
temp_for = forecast['t2m'][:]-273
temp_obs = observation['temperatura'][:]
lats     = np.asarray(observation['lat'][:])
lons     = np.asarray(observation['lon'][:])

# CALCULANDO O RMSE
rmse_temp = aux.rmse(observation=temp_obs, forecast=temp_for, sample=6)

# SALVANDO OS VALORES DO ÍNDICE RMSE EM UM NOVO ARQUIVO NETCDF
data = aux.save_netcdf(data=rmse_temp, times=len(rmse_temp), lats=lats, lons=lons)

# LOOP PARA PLOTAGEM DAS FIGURAS 2D
for i in np.arange(0,len(data),1):
	
	data = np.array(data)
	image = aux.plot_2d(data=data[i], lats=lats, lons=lons, vmin=0, vmax=data.max(), cmap='binary')
	image.title('RMSE da temperatura em 2 metros para o intervalo '+str(i), fontweight='bold', fontsize=10, loc='left')
	image.savefig('plot2D_interval_'+str(i)+'.png', dpi=600, bbox_inches = 'tight')

# PLOTAGEM DA SÉRIE TEMPORAL
aux.plot_xy(xdata=np.arange(0,len(data),1), ydata=data[0:,8,26], xlabel='Intervalos a cada 6 horas',
			    ylabel='RMSE', color='grey', fig_name='SP_RMSE.png' )








