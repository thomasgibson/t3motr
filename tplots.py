import numpy, scipy, matplotlib, cartopy, netCDF4, seaborn, mogreps

from pathlib import Path

forecast_3 = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2015, 12, 5, 15, 0 , 3),data_folder = Path('.'))
forecast_9 = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2015, 12, 5, 9, 0 , 9),data_folder = Path('.'))
forecast_15 = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2015, 12, 5, 3, 0 , 15),data_folder = Path('.'))
forecast_21 = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2015, 12, 4, 21, 0 , 21),data_folder = Path('.'))
forecast_27 = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2015, 12, 4, 15, 0 , 27),data_folder = Path('.'))
forecast_33 = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2015, 12, 4, 9, 0 , 33),data_folder = Path('.'))

DS_forecast_3 = netCDF4.Dataset(forecast_3)
DS_forecast_9 = netCDF4.Dataset(forecast_9)
DS_forecast_15 = netCDF4.Dataset(forecast_15)
DS_forecast_21 = netCDF4.Dataset(forecast_21)
DS_forecast_27 = netCDF4.Dataset(forecast_27)
DS_forecast_33 = netCDF4.Dataset(forecast_33)

forecasts = [DS_forecast_3, DS_forecast_9, DS_forecast_15, DS_forecast_21, DS_forecast_27, DS_forecast_33]

import cartopy.crs as ccrs
from matplotlib import pyplot as plt

def pressure_plots(test_variable, v_min, v_max):
	rotation = forecasts[0]['rotated_latitude_longitude']
	transform = ccrs.RotatedPole(pole_longitude=rotation.grid_north_pole_longitude, pole_latitude = rotation.grid_north_pole_latitude)
	projection = transform
	fig = plt.figure(figsize=(20,10))
	for i in range(0,6):
		ax = fig.add_subplot(2,3,i+1, projection=projection)
		pcm = ax.pcolormesh(
			forecasts[i]['grid_longitude'],
			forecasts[i]['grid_latitude'],
			forecasts[i][test_variable][2],
			transform=transform, vmin = 97000, vmax = 103000, cmap = 'seismic')
		ax.coastlines(resolution='10m')
		ax.set_title(str(6*(i+1)-3)+" hours")
		plt.colorbar(pcm,ax=ax)

def difference_plots(test_variable, v_min, v_max):
	rotation = forecasts[0]['rotated_latitude_longitude']
	transform = ccrs.RotatedPole(pole_longitude=rotation.grid_north_pole_longitude, pole_latitude = rotation.grid_north_pole_latitude)
	projection = transform
	fig = plt.figure(figsize=(20,10))
	for i in range(0,6):
		ax = fig.add_subplot(2,3,i+1, projection=projection)
		pcm = ax.pcolormesh(
			forecasts[i]['grid_longitude'],
			forecasts[i]['grid_latitude'],
			forecasts[i][test_variable][2] - forecasts[0][test_variable][2],
			transform=transform, vmin = v_min, vmax = v_max, cmap = 'seismic')
		ax.coastlines(resolution='10m')
		ax.set_title(str(6*(i+1)-3)+" hours")
		plt.colorbar(pcm,ax=ax)
	
