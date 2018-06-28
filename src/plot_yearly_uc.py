import numpy as np
import netCDF4 as nc
import sys

try:
    data_set = nc.Dataset('uncertainty_output.nc')
except FileNotFoundError:
    print("Data file not found. Run data gathering script.")
    sys.exit()


class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def convert_date(date):

    year = int(date[0:4])
    n = len(date)
    try:
        month = int(date[5:7])
        offset = 7
    except ValueError:
        month = int(date[5:6])
        offset = 6

    day = int(date[offset+1:n])

    return year, month, day


def flatten_data(data_set):

    dates = data_set['date']
    pr_err = np.asarray(data_set['pressure_error'][:]).tolist()
    t_err = np.asarray(data_set['temperature_error'][:]).tolist()
    rain_err = np.asarray(data_set['rainfall_error'][:]).tolist()

    data = AutoVivification()

    for i, date in enumerate(dates):
        year, month, day = convert_date(date)
        data[year][month][day]["pressure_error"] = pr_err[i]
        data[year][month][day]["temperature_error"] = t_err[i]
        data[year][month][day]["rainfall_error"] = rain_err[i]

    return data

data = flatten_data(data_set)
