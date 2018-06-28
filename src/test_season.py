import numpy as np
from mogreps import download_data as download_data
from mogreps import make_data_object_name as make_data
import uncertainty as un
from netCDF4 import Dataset
from pathlib import Path
import os

days = np.arange(2, 10, 1)
times = [9]
years = [2013, 2014, 2015, 2016]
months = [1]
uncertainties = {}
output_name = 'uncertainty_output.nc'

if os.path.isfile('./'+str(output_name)) is not True:
    output_data = Dataset(output_name, 'w')
    output_data.createDimension('id', None)
    output_data.createVariable('date', str, ('id',))
    output_data.createVariable('pressure_error', float, ('id',))
    output_data.createVariable('temperature_error', float, ('id',))
    output_data.createVariable('rainfall_error', float, ('id',))
    output_data.close()
else:
    print('WARNING: adding to existing netcdf file.')

output_data = Dataset(output_name, 'a')
date_array = output_data.variables['date']
p_array = output_data.variables['pressure_error']
T_array = output_data.variables['temperature_error']
r_array = output_data.variables['rainfall_error']


# for now let's do lead time of 27 hours for now
lead_time = 3  # so for a time of 9 and lead time of 9, we are looking at 12pm
month_map = {1: "January",
             2: "Feburary",
             3: "March",
             4: "April",
             5: "May",
             6: "June",
             7: "July",
             8: "August",
             9: "September",
             10: "October",
             11: "November",
             12: "December"}
season_data = {}
year = years[0]

for month in months:
    for day in days:
        for time in times:

            forecast_name = download_data('mogreps-uk',
                                          make_data('mogreps-uk',
                                                    year,
                                                    month,
                                                    day - 1,
                                                    time,
                                                    0,
                                                    lead_time),
                                          data_folder=Path('.'))

            reference_name = download_data('mogreps-uk',
                                           make_data('mogreps-uk',
                                                     year,
                                                     month,
                                                     day,
                                                     time,
                                                     0,
                                                     lead_time),
                                           data_folder=Path('.'))

            try:
                forecast_data = Dataset(forecast_name, 'a')
                reference_data = Dataset(reference_name, 'a')
                measurerer = un.NormalizedErrors(reference_data, forecast_data)
                idx = output_data.dimensions['id'].size

                date_array[idx] = str(year)+'_'+str(month)+'_'+str(day)

                p_array[idx] = measurerer.p_err
                T_array[idx] = measurerer.T_err
                r_array[idx] = measurerer.r_err
            except FileNotFoundError:
                pass


        os.remove(str(forecast_name))
try:
    os.remove("prods*")
except FileNotFoundError:
    print("No files found to delete.")
    pass

print("date", date_array[:])
print("pressure", p_array[:])
print("temperature", T_array[:])
print("rainfall", r_array[:])
