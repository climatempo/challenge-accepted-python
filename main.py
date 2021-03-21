import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

obsFile = 'observation.nc' # Arquivo de observação
fcFile = 'forecast.nc' # Arquivo de previsão

K = 273.15 # Ponto de congelamento da água em Kelvin. Usado para conversão de K -> ºC
nTempos = 72 # Tamanho da série temporal
nIntervalo = 6 # Tamanho do intervalo de horas

obs = xr.open_dataset(obsFile) # Dataset do arquivo de observação
fc = xr.open_dataset(fcFile) # Dataset do arquivo de previsão

# DataArray com o índice RMSE de cada coordenada para cada intervalo
# O cálculo é feito da seguinte forma:
# É feito a conversão de Kelvin para °C no DataArray do arquivo de previsão.
# O resultado é subtraído pelo DataArray do arquivo de observação.
# A diferença é elevada ao quadrado.
# É feito a média aritmética dos intervalos e depois é resolvido o índices que ficaram NaN.
# Por último é feito a raiz quadrada de cada índice.
generalRMSE = np.sqrt((((fc['t2m'] - K) - obs['temperatura']) ** 2).resample(time=f"{nIntervalo}H").mean(dim='time', skipna=False)).ffill(dim='lon')

obsLocal = obs.sel(lat='-23.5489', lon='-46.6388', method='nearest') # Dataset específico da coordenada de SP no arquivo de observação
fcLocal = fc.sel(lat='-23.5489', lon='-46.6388', method='nearest') # Dataset específico da coordenada de SP no arquivo de previsão

# DataArray com o índice RMSE da coordenada de SP para cada intervalo
localRMSE = np.sqrt((((fcLocal['t2m'] - K) - obsLocal['temperatura']) ** 2).resample(time=f"{nIntervalo}H").mean(dim='time', skipna=False))

for x in range(int(nTempos/nIntervalo)): # Geração dos gráficos do Índice RMSE para cada intervalo
    generalRMSE.isel(time=x).plot(cmap='plasma')
    plt.show()

localRMSE.plot() # Geração do gráfico da variação do Índice RMSE nas coordenadas de SP
plt.show()

dsRMSE = generalRMSE.to_dataset(name='RMSE') # Conversão do DataArray com os Índices RMSE gerais para um DataSet
dsRMSE.to_netcdf("RMSE.nc") # Salvamento do DataSet para um arquivo netCDF