import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from netCDF4 import Dataset, num2date
from mpl_toolkits.basemap import Basemap, cm

# Definindo o menor ponto de diferença entre latitudes e longitudes e devolvendo o resultado em x e y.
def latlong(latitudes, longitudes, lat,lon):
   
    x = numpy.argmin(numpy.abs(latitudes - lat))
    y = numpy.argmin(numpy.abs(longitudes - lon))

    return x, y
# Calculo rmse dos pontos de matriz.
def rmse(forecast, target):
    return numpy.sqrt(((forecast - target) ** 2).mean(axis=0))

# Definindo forecast e obversation para ler os arquivos "forcast.nc" e "observation.nc"
forecast = Dataset("forecast.nc")
observation = Dataset("observation.nc")

# Retornando as variaveis com o calculo do rmse em lat e lon.

time = num2date(forecast.variables["time"][:], forecast.variables["time"].units, only_use_cftime_datetimes=False, only_use_python_datetimes=True)
flatitude, flongitude = latlong(forecast.variables["lat"][:], forecast.variables["lon"][:], -23.5489 , -46.6388)
olatitude, olongitude = latlong(observation.variables["lat"][:], observation.variables["lon"][:], -23.5489 , -46.6388)
# Definindo variavel t2m e 
forecast_temp = forecast.variables["t2m"][:]- 273.15
observation_temp = observation.variables["temperatura"][:]
lst = list()
# Função para cortar somente a linha desejada
#root_mean = rmse(forecast_temp[0:7,:,:], observation_temp[0:7,:,:])
#lst.append(root_mean)

# Criar lista com as linhas cortadas para o plot
list_times = list(range(0,73,6))
list_times = list(zip(list_times,list_times[1:]))
end_periods = list()
sao_paulo = list()
# For criado para selecionar as linhas cortadas e selecionar as de 6 em 6 horas
for item in list_times:
    start = item[0]
    end = item[1] + 1

    if end > time.shape[0]:
        end = time.shape[0]

    end_periods.append(time[end-1])

    root_mean = rmse(forecast_temp[start:end,:,:], observation_temp[start:end,:,:])
    sao_paulo.append(root_mean[flatitude, flongitude])

    fig = plt.figure(figsize=(20, 5))

    # Função que projeta a imagem capturada em latitude e longitude 
    map = Basemap()
    X, Y = numpy.meshgrid(forecast.variables["lon"][:], forecast.variables["lat"][:])
    x,y = map(X,Y)
    map = plt.contourf(x, y , root_mean)
    plt.title(f"{time[start]:%Y-%m-%d %H:%M} - {time[end-1]:%Y-%m-%d %H:%M}")
    plt.savefig(f"{time[start]:%Y-%m-%d %H:%M}.png")
    plt.close()



# Plot para São Paulo usando as figuras capturadas e ajustadas.
fig = plt.figure(figsize=(20, 5))
ax = fig.add_subplot(111)

ax.set_xticks(end_periods) 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))

ax.plot_date(end_periods, sao_paulo, ls='-', marker='o')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()
plt.savefig("sao_paulo.png")
plt.show()

