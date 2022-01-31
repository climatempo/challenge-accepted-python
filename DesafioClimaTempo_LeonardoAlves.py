import numpy as np
import netCDF4 as netCDF
import matplotlib.pyplot as matplot
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

#Configurações
ForecastFile = './forecast.nc'
ObservationFile = './observation.nc'

ForecastDS = netCDF.Dataset(ForecastFile, 'r')
#Carregando as variáveis
ForecastLat = ForecastDS.variables['lat'][:]
ForecastLon = ForecastDS.variables['lon'][:]
ForecastTime = ForecastDS.variables['time'][:]
ForecastT2m = ForecastDS.variables['t2m'][:]
#Convertendo Kelvin para Celsius
ForecastT2mC = ForecastT2m
for i in range(len(ForecastT2m)):
    for j in range(len(ForecastT2m[i,:,:])):
        for k in range(len(ForecastT2m[i,j,:])):
            ForecastT2mC[i,j,k]=ForecastT2m[i,j,k]-273.15

ObservationDS = netCDF.Dataset(ObservationFile, 'r')
#Carregando as variáveis
ObservationLat = ObservationDS.variables['lat'][:]
ObservationLon = ObservationDS.variables['lon'][:]
ObservationTime = ObservationDS.variables['time'][:]
ObservationTemperatura = ObservationDS.variables['temperatura'][:]

#Função para realizar o cálculo de forma recursiva
def CalcularRMSE(FC, OB, Periodo=6, Recursivo=True):
    ResultadoRMSE= np.zeros((12,25,37))
    auxResultadoRMSE= np.zeros((72,25,37))
    auxI = 0
    #Correndo os valores de acordo com a janela de dados
    for i in range(len(auxResultadoRMSE)):
        for j in range(len(auxResultadoRMSE[i,:,:])):
            for k in range(len(auxResultadoRMSE[i,j,:])):
                ResultadoRMSE[auxI,j,k] += ((FC[i,j,k]-OB[i,j,k])**2)
        #print("Os valores são auxI", auxI , " i ", i , " j ", j , "k" , k)
        if ((i+1) % Periodo == True) and (i != 0):
            auxI += 1
    #Finalizando o calculo aplicando a raiz em cada coordenada
    ResultadoRMSEsq = ResultadoRMSE
    for i in range(len(ResultadoRMSE)):
        for j in range(len(ResultadoRMSE[i,:,:])):
            for k in range(len(ResultadoRMSE[i,j,:])):
                ResultadoRMSEsq[i,j,k]=np.sqrt(ResultadoRMSE[i,j,k])
    return(ResultadoRMSEsq)

#Função para salvar os dados processados em arquivo
def SalvarNetCDFFile (SalvarArray):
    #Criando o FileDescriptor
    ArqSaida = './LeonardoAlves_Calculo.nc'
    ArqSaidaDS = netCDF.Dataset(ArqSaida, 'w', format='NETCDF4')
    
    PeriodoDim = ArqSaidaDS.createDimension('PeriodoDim', 12)
    RMSELatDim = ArqSaidaDS.createDimension('RMSELatDim', 25)
    RMSELonDim = ArqSaidaDS.createDimension('RMSELonDim', 37)
    
    PeriodoVar = ArqSaidaDS.createVariable('PeriodoDim', 'f4', ('PeriodoDim', ))
    RMSELatVar = ArqSaidaDS.createVariable('RMSELatDim', 'f4', ('RMSELatDim', ))
    RMSELonVar = ArqSaidaDS.createVariable('RMSELonDim', 'f4', ('RMSELonDim', ))
    RMSEValorVar = ArqSaidaDS.createVariable('RMSEValorVar', 'f4', ('PeriodoDim', 'RMSELatDim', 'RMSELonDim', ))
    RMSEValorVar.units = 'Celsius'
    
    RMSEValorVar[:] = SalvarArray[:]
        
    ArqSaidaDS.close()

#Showtime - Executando o código

Calculo = CalcularRMSE(ForecastT2mC, ObservationTemperatura)

SalvarNetCDFFile(Calculo)

