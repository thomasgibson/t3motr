import numpy as np
import mogreps
import uncertainty as un
from netCDF4 import Dataset
from pathlib import Path

days = [19, 20, 21]
days = np.arange(2, 25, 1)
times = [9]
uncertainties = []

# for now let's do lead time of 27 hours for now
lead_time = 3  # so for a time of 9 and lead time of 9, we are looking at 12pm



for day in days:
    for time in times:
        
        forecast_name = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2013, 4, day - 1, time, 0, lead_time), data_folder=Path('.'))
        reference_name = mogreps.download_data('mogreps-uk', mogreps.make_data_object_name('mogreps-uk', 2013, 4, day, time, 0, lead_time), data_folder=Path('.'))
        forecast_data = Dataset(forecast_name, 'a')
        reference_data = Dataset(reference_name, 'a')
        measurerer = un.NormalizedErrorAirPressure(reference_data, forecast_data)
        uncertainties.append(measurerer.norm_err)


print(uncertainties)
        
