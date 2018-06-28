import numpy as np
from mogreps import download_data as download_data
from mogreps import make_data_object_name as make_data
import uncertainty as un
from netCDF4 import Dataset
from pathlib import Path
import os

days = np.arange(1, 31, 1)
times = [15]
years = [2013, 2014, 2015, 2016]
months = np.arange(1, 12, 1)
ensembles = np.arange(1, 12, 1)

output_name = 'ensemble_output.nc'

if os.path.isfile('./'+str(output_name)) is not True:
    output_data = Dataset(output_name, 'w')
    output_data.createDimension('id', None)
    output_data.createDimension('member', 12)
    output_data.createVariable('date', str, ('id',))
    output_data.createVariable('pressure_error', float, ('id', 'member', ))
    output_data.createVariable('temperature_error', float, ('id', 'member', ))
    output_data.createVariable('rainfall_error', float, ('id', 'member', ))
    output_data.close()
else:
    print('WARNING: adding to existing netcdf file.')

output_data = Dataset(output_name, 'a')
date_array = output_data.variables['date']
p_array = output_data.variables['pressure_error']
T_array = output_data.variables['temperature_error']
r_array = output_data.variables['rainfall_error']


# for now let's do lead time of 27 hours for now
lead_time = 27  # so for a time of 9 and lead time of 9, we are looking at 12pm

for year in years:
    for month in months:
        for day in days:
            for time in times:

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
                    # check that the reference data exists
                    reference_data = Dataset(reference_name, 'r')                    

                    idx = output_data.dimensions['id'].size
                    date_array[idx] = str(year)+'_'+str(month)+'_'+str(day)
                    
                    for ensemble in ensembles:

                        forecast_name = download_data('mogreps-uk',
                                                      make_data('mogreps-uk',
                                                                year,
                                                                month,
                                                                day,
                                                                time,
                                                                ensemble,
                                                                lead_time),
                                                      data_folder=Path('.'))

                        # check that the ensemble member exists
                        try:

                            forecast_data = Dataset(forecast_name, 'r')
                            measurerer = un.NormalizedErrors(reference_data, forecast_data)
                            p_array[idx, ensemble-1] = measurerer.p_err
                            T_array[idx, ensemble-1] = measurerer.T_err
                            r_array[idx, ensemble-1] = measurerer.r_err

                            os.remove(str(forecast_name))

                        except (OSError, FileNotFoundError):
                            p_array[idx, ensemble-1] = np.nan
                            T_array[idx, ensemble-1] = np.nan
                            r_array[idx, ensemble-1] = np.nan
                    

                    os.remove(str(reference_name))

                except (OSError, FileNotFoundError):
                    pass

print("date", date_array[:])
print("pressure", p_array[:,:])
print("temperature", T_array[:,:])
print("rainfall", r_array[:,:])
