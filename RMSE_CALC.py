# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 07:57:46 2021

@author: thela
"""

import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import datetime
import os
from netCDF4 import Dataset as NetCDFFile 
import netCDF4 as nc
import glob
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import seaborn as sns
import matplotlib.ticker as tick

sns.set_style("whitegrid")

#Função que Calcula o RMSE
def calc_rmse(intervalo,observado,previsto,escala):
    rmse= []
    for i in np.arange (0,len(previsto),intervalo):
        var= np.sum((np.power((observado[i:i+intervalo] - previsto[i:i+intervalo]),2)), axis=0)/intervalo
        rmse.append(np.sqrt(var))
    return rmse


#Função que plota e salva o contorno da RMSE para o intervalo de 6h 
def plot_contour(lon_obs, lat_obs, rmse_cal,time_range,lv_min,lv_max):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.set_extent([lon_obs[-1], lon_obs[0], lat_obs[-1], lat_obs[0]], ccrs.PlateCarree())
    label=time_range.strftime('%d %m %Y %H:%M')
    states = cfeature.NaturalEarthFeature(category='cultural',
                                          name='admin_1_states_provinces_shp',
                                          scale='50m',
                                          facecolor='none')  
    ax.add_feature(states, edgecolor='black', linestyle=':', linewidth=1)
    grid= ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--', linewidth=2)
    grid.xlabels_top = False
    grid.ylabels_right = False
    grid.xlabel_style = {'size': 10}
    grid.ylabel_style = {'size': 10}
    levels = np.linspace(int(lv_min), int(lv_max), 10)
    contour=plt.contourf(lon_obs, lat_obs, rmse_cal, transform=ccrs.PlateCarree(),cmap = 'jet',levels=levels)
    plt.title('Contorno do RMSE entre a temperatura observada e prevista para São Paulo em '+'\n'+str(time_range), fontweight='bold', fontsize=10)
    fig.colorbar(contour,orientation='horizontal',label = 'RMSE entre a temperatura observada e prevista', aspect=50,format=tick.FormatStrFormatter('%.1f'))
    plt.savefig('Contorno do RMSE da temperatura para o dia ' + label + '' '.jpeg',dpi=200,bbox_inches = "tight")

#Função que cria um arquivo de saida da RMSE em formato NETCDF
def netcdf_creator(data,lats,lons,path_save):
    
    fn = path_save
    rmse_cal_aux= np.asarray(data)
    intervalos = np.arange(0,len(data),1)
    ds = nc.Dataset(fn, 'w', format='NETCDF4') 
    tempo = ds.createDimension('tempo', len(intervalos))
    new_lat = ds.createDimension('new_lat', len(lats))
    new_lon = ds.createDimension('new_lon', len(lons))
    temp_var = ds.createVariable('tempo', 'f4', ('tempo'))
    lats = ds.createVariable('lats',  'f4', ('new_lat'))
    lons = ds.createVariable('lons',  'f4', ('new_lon'))
    value = ds.createVariable('RMSE_t2m',  'f4', ('tempo', 'new_lat', 'new_lon'))
    tempo_var = ds.createVariable('tempo_var', 'f4', ('tempo'))
    tempo_var[:] = intervalos
    lats[:] = lats[:]
    lons[:] = lons[:]
    value[:, :, :] = rmse_cal_aux
    print('New NETCDF has the shape: ', value.shape)
    return value

#Função que plota e salva um grafico de linha da variação da RMSE para um determinado ponto    .  
def plot_timeserie (data,indice_x,indice_y,time_range,lat_ref,lon_ref):
    line_data=pd.DataFrame({"RMSE":data[0:,indice_y,indice_x]})
    line_data.set_index(time_range, inplace = True)
    fig=plt.figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
    ax = sns.lineplot(data=line_data, x=line_data.index, y="RMSE",linewidth = 5)
    ax.set_xticklabels(line_data.index.strftime('%d-%m-%Y %H:%M'),fontsize=12)
    plt.title('Variação Da RMSE Temperatura a cada 6H nas coordenadas: latitide:'+str(lat_ref)+" e longitude: "+str(lon_ref), weight='bold',fontsize=20)
    ax.tick_params(labelsize=5)
    ax.set_xlabel('DateTime',fontsize=20,weight='bold')
    ax.set_ylabel('RMSE Temperatura',fontsize=20,weight='bold')
    plt.xticks(fontsize=15,weight='bold')
    plt.yticks(fontsize=15,weight='bold')
    fig.set_size_inches((8, 8), forward=False)
    plt.savefig('Variação Da RMSE Temperatura a cada 6H ')
    plt.show()
    
    
    
    
    

path_entrada = r'D:/challenge' # caminho da pasta onde os arquivos estão salvos
try:
    all_files = glob.glob(path_entrada  + "/*.nc") # Aqui ele verifica se foi dado um caminho e caso não,
                                         #coleta os arquivos onde o arquivo .py esta salvo#
except:
    all_files = glob.glob(os.getcwd() + "/*.nc")

#Aqui podemos definir onde salvar o arquivo Netcdf de saida.
#É interessante salvar em outro lugar que os arquivos de entrada, nos casos de rodas o script varia vezes
#Nesse passo, para evitar  erros de gravação, caso ja exista o arquivo ele é deletado.
path_save = 'C:/temp/test.nc'  
if os.path.exists(path_save):
  os.remove(path_save)


#lendo o arquivo Netcdf
forecast=NetCDFFile (all_files[0])
observation=NetCDFFile (all_files[1])

#Extraindo as variaveis de interesse

t2m_obs=(observation["temperatura"][:])
t2m_fcst=(forecast["t2m"][:])-273.15
lat_obs=np.asarray(observation['lat'][:])
lon_obs=np.asarray(observation['lon'][:])

#Seleciona as coordenadas para criação do grafico de linha.
coord_x=26
coord_y=8
lat_ref=-23.5489
lon_ref=-46.6388


#Aqui o programa coleta e formada um range de datas para que eles sejam usados nos graficos
time_var = forecast.variables['time']
dtime = nc.num2date(time_var[:],time_var.units)
min_dates=dtime[0]
max_dates=dtime[-1]
min_dates=datetime.datetime.strptime(str(min_dates), "%Y-%m-%d %H:%M:%S")
max_dates=datetime.datetime.strptime(str(max_dates), "%Y-%m-%d %H:%M:%S")
time_range = pd.date_range(min_dates, max_dates, freq= "6H")

rmse_cal=calc_rmse(6,t2m_obs,t2m_fcst,"6H")
rmse_cal=np.array(rmse_cal)
contour_plots=[]
min_value=[]
max_value=[]

#Procura o maior e menor valor dentre todos os arrays, para fixar a escala de cor dos contornos.
#Assim evidanto que cada contorno tenha um range de escala e possa gerar más interpretações.
for i in np.arange(0,len(rmse_cal),1):
    min_value.append(min([min(p) for p in rmse_cal[i]]))
    max_value.append(max([max(p) for p in rmse_cal[i]]))
    



#plota os contornos
for i in np.arange(0,len(rmse_cal),1):
  plot_contour(lon_obs, lat_obs, rmse_cal[i],time_range[i],min(min_value),max(max_value))
  
nc=netcdf_creator(rmse_cal,lat_obs,lon_obs,path_save)
plot_timeserie(nc,coord_x,coord_y,time_range,lat_ref,lon_ref)

