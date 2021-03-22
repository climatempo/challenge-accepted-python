import netCDF4 as nc
import source

if __name__ == '__main__':
    forecast = nc.Dataset('forecast.nc')
    observation = nc.Dataset('observation.nc')
    source.teste(forecast, observation)

    infos = source.nc_to_dict(forecast, observation)
    source.plot_time_series(infos, 8, 26, 6)