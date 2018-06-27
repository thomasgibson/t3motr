import numpy as np
import mogreps
import uncertainty as un
from netCDF4 import Dataset
from pathlib import Path
import os

days = np.arange(2, 31, 1)
times = [9]
years = [2013, 2014, 2015, 2016]
month = 1
uncertainties = {}

# for now let's do lead time of 27 hours for now
lead_time = 3  # so for a time of 9 and lead time of 9, we are looking at 12pm

for day in days:
    for time in times:
        forecast_name = mogreps.download_data('mogreps-uk',
                                              mogreps.make_data_object_name('mogreps-uk', year,
                                                                            month, day - 1,
                                                                            time, 0, lead_time),
                                              data_folder=Path('.'))
        reference_name = mogreps.download_data('mogreps-uk',
                                               mogreps.make_data_object_name('mogreps-uk', year,
                                                                             month, day,
                                                                             time, 0, lead_time),
                                               data_folder=Path('.'))

        try:
            forecast_data = Dataset(forecast_name, 'a')
            reference_data = Dataset(reference_name, 'a')
            measurerer = un.NormalizedErrorAirPressure(reference_data, forecast_data)
            uncertainties[(day, time)] = measurerer.norm_err
        except FileNotFoundError:
            pass

        os.remove(str(forecast_name))
os.remove(str(reference_name))

print("July", np.mean(list(uncertainties.values())))
        
