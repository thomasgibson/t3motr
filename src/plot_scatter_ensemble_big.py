from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
from matplotlib.dates import date2num, YearLocator, MonthLocator, DateFormatter
import matplotlib.pyplot as plt
import time
import datetime
from scipy import optimize
from math import isnan, pi

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

data = Dataset('ensemble_output.nc', 'r')

variables = ['pressure_error', 'rainfall_error']

labels = ['Pressure', 'Rainfall']

dates_raw = data.variables['date']
dates = []

# convert dates
for i in range(len(dates_raw[:])):
    year, month, day = convert_date(dates_raw[i])
    dt = datetime.datetime(year=year, month=month, day=day)
    dates.append(date2num(dt))

years = YearLocator()
months = MonthLocator()
yearsFmt = DateFormatter('%Y')

FONTSIZE = 12

for variable, title in zip(variables, labels):

    error = data.variables[variable][:,:]
    full_dates = []
    full_error = []

    for i in range(len(error)):
        for j in range(len(error[i])):
            if isnan(error[i,j]):
                pass
            else:
                full_dates.append(dates[i])
                full_error.append(error[i, j])
            

    plt.close()

    # make individual plot
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    ax.scatter(full_dates, full_error, color='black', marker='.', s=0.2)

    # set labels
    ax.set_xlabel(r'Date', fontsize=FONTSIZE)
    ax.set_ylabel(r'Normalised Error', fontsize=FONTSIZE)
    ax.set_title(title, fontsize=FONTSIZE)

    # edit axis ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    data_range = 0.05 * (np.max(full_error) - np.min(full_error))
    ax.set_ylim([np.min(full_error) - data_range, np.max(full_error) + data_range]) 

    ax.grid(b=True, which='major', linestyle='-.')
    fig.savefig('ensemble_scatter_'+str(variable)+'.pdf',
                orientation="landscape",
                transparent=True,
                bbox_inches='tight')
    
