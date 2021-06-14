# Script do Challenge de Python da Climatempo
# Este script calcula o RMSE de duas fontes de dados, a cada 6 horas, plota os mapas dos índices e 
# gera um gráfico do índice para São Paulo
# Autora: Brenda A. Santos
# Data: 12 junho de 2021

# Importações necessárias
import xarray as xr
import pandas as pd
import proplot as plot
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader

# Definição de constantes
FREQUENCIA_TEMPO = '6H'
DIMENSAO = 'time'
CIDADE_REFERENCIA = 'São Paulo'
LATITUDE_REFERENCIA = -23.5489
LONGITUDE_REFERENCIA = -46.6388
RESOLUCAO_IMG = 300

prev = xr.open_dataset('forecast.nc')['t2m']-273.15
obser = xr.open_dataset('observation.nc')['temperatura']

# Carregando o arquivo shapefile com a divisão dos estados
arq_shp = 'UFEBRASIL'

# Igualando as coordenadas de latitude e longitude - tinha diferença na casa decimal
prev.coords['lat'] = obser.lat
prev.coords['lon'] = obser.lon

# Criando uma lista vazia para colocar o resultado
lista_result = []

# Determinando a frequencia fixa de 6 horas para cálculo do índice
intervalo_tempo = pd.date_range(prev.time[0].values, prev.time[-1].values, freq= FREQUENCIA_TEMPO)

# Calculando o RMSE
for tempo in intervalo_tempo:
    prev_6h = prev.sel(time = slice(pd.Timestamp(str(tempo)), pd.Timestamp(str(tempo)) + pd.Timedelta(FREQUENCIA_TEMPO)))
    obser_6h = obser.sel(time = slice(pd.Timestamp(str(tempo)), pd.Timestamp(str(tempo)) + pd.Timedelta(FREQUENCIA_TEMPO)))
    rmse_6h = ((((prev_6h - obser_6h) ** 2).mean(dim = DIMENSAO) ** 0.5).assign_coords(time = tempo).expand_dims(DIMENSAO))
    lista_result.append(rmse_6h)

# Criando um arquivo netcdf com o resultado
rmse_ds = xr.concat(lista_result, dim = DIMENSAO)
rmse_ds.to_netcdf('RMSE_6H.nc')
       
# Gerando os mapas do índice de cada período
for tempo in intervalo_tempo:
	rmse_result = rmse_ds.sel(time = str(tempo))
	
	fig, axs = plot.subplots(axheight = 5, tight = True, proj = 'pcarree')
	axs.format(coast = True, borders = True, latlim = (min(rmse_ds.lat), max(rmse_ds.lat)), 
	lonlim = (min(rmse_ds.lon), max(rmse_ds.lon)), labels=True, title='Índice RMSE ' + str(tempo))
	mapa = axs.contourf(rmse_result, cmap = 'Blues', vmin = 0, vmax = 5)
	fig.colorbar(mapa,label = 'RMSE da temperatura')
	
	# Adicionando divisao estados
	shape_feature = ShapelyFeature(shpreader.Reader(arq_shp).geometries(),\
	ccrs.PlateCarree(), facecolor='none', edgecolor='k', linewidth=0.5)
	axs.add_feature(shape_feature)

	fig.save(str(tempo) + '_RMSE.png', dpi = RESOLUCAO_IMG)
	
# Série temporal do índice rmse, a cada 6h, para São Paulo
rmse_sp = rmse_ds.sel(lon = LONGITUDE_REFERENCIA, lat = LATITUDE_REFERENCIA, method='nearest')

# Plotando a série
graf, ax = plot.subplots(figsize = (7, 3), tight = True)
ax.plot(rmse_sp['time'], rmse_sp, marker = 'o')
ax.format(xlabel = 'Tempo', ylabel = 'Índice RMSE',
title = 'Índice RMSE da temperatura para ' + CIDADE_REFERENCIA)
graf.save('RMSE_' + CIDADE_REFERENCIA + '.png')
 
 
