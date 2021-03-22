import netCDF4 as nc
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os

def teste(d1,d2):
    assert d1.dimensions['lat'].size == d2.dimensions['lat'].size, "Shapes diferentes de latitude"
    assert d1.dimensions['lon'].size == d2.dimensions['lon'].size, "Shapes diferentes de longitude"
    assert d1.dimensions['time'].size == d2.dimensions['time'].size, "Shapes diferentes de tempo"
    print("Aprovado em todos os testes")

def get_times(nc_object):
    """ Retorna um datetime com todos os horário possíveis no arquivo. A partir da data de início, fornece os outros horários de hora em hora. """
    inicial_date = dt.datetime.strptime(nc_object['time'].units[-18:], '%Y-%m-%d %H:%M:%S')
    times = [inicial_date + dt.timedelta(hours=t) for t in range(nc_object.dimensions['time'].size)]
    return times

def get_time_index(tempos, r):
    """ Percorre uma lista de datetimes e retorna o indíce em que os horário dentro de um range aparecem.
    
    Parâmetros
    ----
    * tempos :: list()  
        lista de datetimes.
    * r :: int, hora
        Passo que a busca irá acontecer. 
    """
    start = tempos[0]
    end = tempos[-1]
    i = 0
    atual = start
    idx = list()
    #import pdb; pdb.set_trace()
    while (atual+dt.timedelta(hours=r)) < end:
        atual = start + i*dt.timedelta(hours=r)
        idx.append(tempos.index(atual))
        i+=1
    return idx

def get_RMSE(array1, array2):
    """ Calcula o indice RMSE entre dois vetores. """
    RMSE = np.nanmean((array1 - array2)**2)
    return RMSE

def compare_single_place(dados, r, lat, lon):
    """ Está função calcula o RMSE entre a temperatura predita e temperatura real para uma localidade (`lat`, `lon`), em cada intervalo de tempo determinado por `r`.
    
    Parâmetros
    ----
    * dados :: dict()
        Dicionário com informação consolidade dos arquivos .nc
    * r :: int, hora
        Passo que a busca irá acontecer. 
    * lat :: int
        Posição que no vetor de latitudes.
    * lon :: int
        Posição no vetor de longitudes.

    Retorno
    ---
    * res :: dict()
        Dicionário no formato { Indice do horário analisado -> RMSE da temperatura }
    """
    times_idx = get_time_index(dados['times'], r)
    forecast_data = dados['lat_'+str(lat)+'_lon_'+str(lon)]['t2m_f'][times_idx] - 273.15
    observed_data = dados['lat_'+str(lat)+'_lon_'+str(lon)]['temp_o'][times_idx]
    RMSE = list(map(get_RMSE, forecast_data,observed_data))
    res = dict(zip(times_idx,RMSE))
    return res

def compare_all_places(dados, r):
    """ Está função calcula o RMSE entre a temperatura predita e temperatura real para todas as localidades dos arquivos .nc, em cada intervalo de tempo determinado por `r`.
    
    Parâmetros
    ----
    * dados :: dict()
        Dicionário com informação consolidade dos arquivos .nc
    * r :: int, hora
        Passo que a busca irá acontecer.

    Retorno
    ---
    * res :: dict()
        Dicionário no formato { Indice do horário analisado -> RMSE da temperatura }
    """
    times_idx = get_time_index(dados['times'], r)
    temp_pred = np.array([dados[key]['temp_o'][times_idx] for key in dados.keys() if key != 'times'])
    temp_true = np.array([dados[key]['t2m_f'][times_idx] - 273.15 for key in dados.keys() if key != 'times'])

    res = dict()
    for time in range(temp_pred.shape[1]):
        res[time*r] = get_RMSE(temp_pred[:,time], temp_true[:,time])
    return res

def plot_time_series(dados,lat, lon, r):
    """ Cria e salva um gráfico de séries temporais para determinada localidade (lat,lon) em cada intervalo de tempo determinado por `r`. O indíce RMSE em cada intervalo de tempo.

    Parâmetros
    ----
    * dados :: dict()
        Dicionário com informação consolidade dos arquivos .nc
    * r :: int, hora
        Passo que a busca irá acontecer. 
    * lat :: int
        Posição que no vetor de latitudes.
    * lon :: int
        Posição no vetor de longitudes.
    """
    single = compare_single_place(dados, r, lat, lon)
    times_index = [key for key in single.keys()]
    vals = np.fromiter(single.values(), dtype=float)
    
    xt = dados['times'][0:-1:6]
    size = len(times_index)
    t_pred = dados['lat_'+str(lat)+'_lon_'+str(lon)]['t2m_f'][times_index] - 273.15
    t_true = dados['lat_'+str(lat)+'_lon_'+str(lon)]['temp_o'][times_index]
    
    # multiple line plots
    plt.figure(figsize=(15,8))
    plt.plot( range(size) , t_pred, color='orange', label="Forecast")
    plt.plot( range(size), t_true, color='blue', label="Observed")
    plt.errorbar(range(size), t_true, yerr=0.3, label="RMSE");
    for i in range(size):
        plt.text(i, t_true[i]+0.2, '{:.3f}'.format(vals[i]))

    plt.xticks(range(size),labels=xt,rotation=50)
    plt.ylabel("Temperatura em ºC")
    lat_ = dados['lat_'+str(lat)+'_lon_'+str(lon)]['lat']
    lon_ = dados['lat_'+str(lat)+'_lon_'+str(lon)]['lon']
    plt.title(f"Série temporal das temperaturas observadas e preditas para a cidade em (lat: {lat_}, lon: {lon_})")

    # show legend
    plt.legend(loc='upper right', ncol=1)
    plt.grid(True)
    plt.savefig("time_series.png")
    #plt.show()

def nc_to_dict(forecast, observation):
    """ Consolida as informações de arquivos .nc em um dicionário. """

    infos = dict()
    infos['times'] = get_times(forecast)

    for i in range(forecast.dimensions['lat'].size):
        for j in range(forecast.dimensions['lon'].size):
            infos[f'lat_{i}_lon_{j}'] = {
                'lat' : forecast['lat'][i].data,
                'lon' : forecast['lon'][j].data,
                't2m_f' : forecast['t2m'][:,i,j].data,
                'temp_o' : observation['temperatura'][:,i,j].data,
            }
    return infos