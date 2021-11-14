#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROCESSO DE RECRUTAMENTO PARA DESENVOLVEDORES PYTHON - CLIMATEMPO

AUTOR DO SCRIPT: DOUGLAS LIMA DE BEM 

DATA: 14/11/2021
"""

import netCDF4 as nc
import numpy as np 
import math
import cartopy, cartopy.crs as ccrs        # Plot maps
import cartopy.io.shapereader as shpreader # Import shapefiles
import matplotlib.pyplot as plt            # Plotting library
import matplotlib                          # Comprehensive library for creating static, animated, and interactive visualizations in Python 
import pandas as pd 
from netCDF4 import Dataset

interval = 6

################ LAT/LON PARA A CIDADE DE SÃO PAULO ###########################
lat_SP = -23.5489
lon_SP = -46.6388
####### LEITURA DOS DADOS FORECAST/OBSERVATION E SET DAS VARIÁVEIS ############

''' Leitura dos arquivos necessários'''
forecast = 'forecast.nc'
observacao = 'observation.nc'
#------------------------------------------------------------------------
''' Indicando as variáveis usadas para encontrar o RMSE e para plotagem '''
ds_F = nc.Dataset(forecast)
ds_O = nc.Dataset(observacao)
time =  ds_F['time'][:]
lon = ds_F['lon'][:]
lat = ds_F['lat'][:]
t2m_F = ds_F['t2m'][:] - 273.15
t2m_O = ds_O['temperatura'][:]
#------------------------------------------------------------------------
'''Devido ao fato de termos dois valores "nan" no observado, precisa-se o uso de uma máscara ajustando o valor da T2m'''
t2m_ajustada = np.ma.masked_array(t2m_O,np.isnan(t2m_O))
#------------------------------------------------------------------------
######### VARIAÇÃO DO RMSE PARA O INTERVALO DE 6 HORAS #####################

'''Cálculo do RMSE para cada intervalo de 6 horas para todas lat/lon'''
for i in range(0,t2m_F.shape[0],interval):
    
    mse = ((t2m_ajustada[i,:,:]-t2m_F[i,:,:])**2)  
    rmse = np.sqrt(mse) 

#------------------------------------------------------------------------      
############# PLOT MAPA PARA ESTADO DE SÃO PAULO ###########################   

    '''Tamanho da figura a qual será plotada'''
    plt.figure(figsize=(13,13))
#------------------------------------------------------------------------    
    ''' Projeção usada '''
    ax = plt.axes(projection=ccrs.PlateCarree())
#------------------------------------------------------------------------
    ''' Shapefile para as divisões territoriais do Brasil '''  
    shapefile = list(shpreader.Reader('shapefile/BR_UF_2019.shp').geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=0.3)
    ax.coastlines(resolution='10m', color='black', linewidth=0.8)
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
#------------------------------------------------------------------------   
    '''Definição de um intervalo e dos valores máximos e mínimos de RMSE '''
    data_min = 0
    data_max = 5
    interval = 0.5
    levels = np.arange(data_min,data_max,interval)
 #------------------------------------------------------------------------      
    '''Plotagem dos valores'''
    img1 = ax.contourf(lon[:], lat[:], rmse[:,:], cmap=plt.cm.RdBu_r, extend='both',levels=levels)  
    img2 = ax.contour(lon[:], lat[:], rmse[:,:], colors='white', linewidths=0.3,levels=levels)
 #------------------------------------------------------------------------     
    '''Inserção da Escala de cores'''
    plt.colorbar(img1, label='RMSE', orientation='horizontal', pad=0.05, fraction=0.05)    
#------------------------------------------------------------------------
    '''Inserção do título'''
    plt.title('RMSE para Temperatura à 2 metros' , fontweight='bold', fontsize=10, loc='left')
 #------------------------------------------------------------------------   
    '''Inserção do ponto na cidade de São Paulo (Adicional) '''
    plt.plot([lon_SP],[lat_SP],color='black',linewidth = 3, marker='o', transform=ccrs.PlateCarree())        
    plt.text(lon_SP, lat_SP - 0.2, 'São Paulo (SP)',c='black',fontsize = 'large', horizontalalignment = 'center', transform=ccrs.Geodetic())
#------------------------------------------------------------------------    
    '''Salvando as figuras a partir da variação temporal'''
    plt.savefig('RMSE_T2m_' + str(time[i]).split('.')[0] + '.png', bbox_inches='tight', pad_inches=0, dpi=600)
#------------------------------------------------------------------------          
    plt.close('all')
############# PLOT SÉRIE TEMPORAL (SÃO PAULO) ##############################
'''Cria um DataFrame para inserir os valores de RMSE para cidade de São Paulo'''    
dados = pd.DataFrame()
#------------------------------------------------------------------------ 
'''Cálculo do RMSE para cada intervalo de 6 horas para lat/lon de SP'''
for i in range(0,t2m_F.shape[0],6):

    MSE = np.square(np.subtract(t2m_ajustada[i,8,26], t2m_F[i,8,26])).mean()
    RMSE = math.sqrt(MSE)   
    d = {'RMSE': RMSE, 'Tempo (intervalo a cada 6 horas)': i}
    dados = dados.append(d,ignore_index=True)
#------------------------------------------------------------------------ 
'''Tamanho do da figura a qual será plotada'''
plt.figure(figsize=(13,13))
#------------------------------------------------------------------------ 
dados = dados.set_index('Tempo (intervalo a cada 6 horas)')

'''Plotagem dos dados indexiados no DataFrame'''
dados.RMSE.plot(color='red',grid = True, linestyle ='dashed') 
#------------------------------------------------------------------------ 
'''Salvando a figura a partir da série temporal'''
plt.savefig('RMSE.png', bbox_inches='tight', pad_inches=0, dpi=600)