import numpy as np 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset

def rmse(observation, forecast, sample):

	rmse_temp = []
	for i in np.arange(0,len(observation),sample):

		index = (np.sum(((observation[i:i+sample] - forecast[i:i+sample])**2), axis=0)/sample)**0.5
		rmse_temp.append(index)

	return rmse_temp

def save_netcdf(data, times, lats, lons):

	data = np.asarray(data)
	times = np.arange(0,times,1)
	dataset = Dataset('rmse.nc', 'w', format='NETCDF4_CLASSIC')
	nlat = dataset.createDimension('nlat', len(lats))
	nlon = dataset.createDimension('nlon', len(lons))
	ntime = dataset.createDimension('ntime', len(times))
	rmse = dataset.createVariable('rmse', np.float32, ('ntime','nlat','nlon'))
	time = dataset.createVariable('time', np.float32, ('ntime'))
	latitude = dataset.createVariable('latitude', np.float32, ('nlat'))
	longitude = dataset.createVariable('longitude', np.float32, ('nlon'))
	rmse[:,:,:] = data
	time[:] = times
	latitude[:] = lats
	longitude[:] = lons 

	return rmse

def plot_2d(data, lats, lons, vmin, vmax, cmap):

	import cartopy, cartopy.crs as ccrs
	import cartopy.feature as cfeature
	import matplotlib.pyplot as plt
	from netCDF4 import Dataset
	import numpy as np
	from cartopy.feature import NaturalEarthFeature, BORDERS
	
	datacrs = ccrs.PlateCarree()
	img_extent = (lons.min(), lons.max(), lats.min(), lats.max())
	plt.figure(figsize=(7,7))

	ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=-103.3))#, globe=globe))
	ax.set_extent([lons.min(), lons.max(), lats.min()+.2, lats.max()-.2], crs=ccrs.PlateCarree())

	ax.stock_img()
	states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none', name='admin_1_states_provinces_shp')
	ax.add_feature(states, edgecolor='brown', linewidth=1.4)

	ax.add_feature(cfeature.BORDERS, edgecolor='white', linewidth=1.2)
	gl = ax.gridlines(color='gray', alpha=0.5, linestyle='--', linewidth=0.5, draw_labels=True)
	gl.xlabels_top   = False
	gl.ylabels_right = False
	img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='upper', extent=img_extent, cmap=cmap, transform=datacrs)
	plt.colorbar(img, label='RMSE', extend='both', orientation='horizontal', pad=0.05, fraction=0.05)

	return plt

def plot_xy(xdata, ydata, xlabel, ylabel, color, fig_name):

	fig, ax = plt.subplots()
	ax.set_xlabel(xlabel, weight='bold', size=13)
	ax.set_ylabel(ylabel, weight='bold', size=13)
	plt.grid(True, color=color, linestyle=':')
	plt.setp(ax.get_xticklabels(), size=10)
	ax.plot(xdata, ydata, 'r-', linewidth=3)
	plt.savefig(fig_name, dpi=600, bbox_inches = 'tight')
	




















