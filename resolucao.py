# Importações necessárias
import xarray as xr
import pandas as pd
import proplot as pplot

# Definição de Constantes
REFERENCIA_CIDADE = 'São Paulo'
REFERENCIA_LATITUDE = -23.5489
REFERENCIA_LONGITUDE = -46.6388
FREQUENCIA_TEMPO = '6H'
DIMENSAO_ESTUDO = 'time'

##Leitura dos arquivos NC
dadosPrevisao = xr.open_dataset('forecast.nc')['t2m']-273.15
dadosObservados = xr.open_dataset('observation.nc')['temperatura']

## Identifiquei que haviam algumas diferenças nas casas deciamais das coordenadas
## Foi necessário igualar os dados para prosseguir com as operações
## Caso não tivesse igualado os dados haveriam apenas 3600 linhas de dados pra serem comparadas
dadosPrevisao.coords['lat'] = dadosObservados.lat
dadosPrevisao.coords['lon'] = dadosObservados.lon


## Lista vazia que recebera os resultados
listaResultados = []

## Cria um indice de intervalos de tempo com frequencia de 6 horas
intervaloTempo = pd.date_range(dadosPrevisao.time[0].values, dadosPrevisao.time[-1].values, freq = FREQUENCIA_TEMPO)


## Calculando o RMSE
for tempo in intervaloTempo:
    
    ##Seleciona os dados dentro do intervalo de Tempo
    fimPeriodo      = pd.Timestamp(str(tempo)) + pd.Timedelta(FREQUENCIA_TEMPO)
    previsao6Hrs    = dadosPrevisao.sel(time = slice(pd.Timestamp(str(tempo)),fimPeriodo))
    observados6Hrs  = dadosObservados.sel(time = slice(pd.Timestamp(str(tempo)),fimPeriodo))
    
    ##Calcula o indice rmse para oa dados do intervalo
    rmse6hrs = (((previsao6Hrs - observados6Hrs) ** 2).mean(dim = DIMENSAO_ESTUDO) ** 0.5).assign_coords(time = tempo).expand_dims(DIMENSAO_ESTUDO)
    
    listaResultados.append(rmse6hrs)


## Transforma a Lista de resultados pro formato netcdf e salva no computador
resultadosRmse = xr.concat(listaResultados, dim = DIMENSAO_ESTUDO)
resultadosRmse.to_netcdf('RMSE_6H_RESULTADOS')

## Cria a serie temporal para a Cidade de São Paulo do Indice RMSE com intervalos de 6Hrs
rmseSP = resultadosRmse.sel(lon = REFERENCIA_LONGITUDE, lat = REFERENCIA_LATITUDE, method = 'nearest')

## Plotando a série Temporal de SP
grafsp, ax = pplot.subplots()
ax.plot(rmseSP['time'], rmseSP, marker = '.')
ax.format(xlabel = 'Tempo', ylabel = 'Índice RMSE', title = 'Índice RMSE da temperatura de ' + REFERENCIA_CIDADE)
grafsp.save('RMSE ' + REFERENCIA_CIDADE + '.png')

for tempo in intervaloTempo:
    ## Selecionando os dados com base do Intervalo de Tempo
    resultadoRmse = resultadosRmse.sel(time = str(tempo))
    ##plotando a série temporal
    figuraRmse, axs = pplot.subplots(axheight = 5, tight = True)
    axs.format(coast = True, borders = True, latlim = (min(resultadosRmse.lat), max(resultadosRmse.lat)), 
            lonlim = (min(resultadosRmse.lon), max(resultadosRmse.lon)), labels=True, title='Índice RMSE ' + str(tempo))
    figuraRmse.save(str(tempo).replace(':','').replace('-','').replace(' ','_') + '_RMSE.png')
