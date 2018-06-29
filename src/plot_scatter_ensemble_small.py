from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
from matplotlib.dates import date2num, YearLocator, MonthLocator, DateFormatter, DayLocator
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

dates_raw = data.variables['date'][40:50]
dates = []

# convert dates
for i in range(len(dates_raw[:])):
    year, month, day = convert_date(dates_raw[i])
    dt = datetime.datetime(year=year, month=month, day=day)
    dates.append(date2num(dt))

years = YearLocator()
months = MonthLocator()
monthsFmt = DateFormatter('%d/%m')
days = DayLocator()

FONTSIZE = 12

for variable, title in zip(variables, labels):

    error = data.variables[variable][40:50,:]
    dates_matrix = []
    full_error = []

    for i in range(len(error)):
        dates_matrix.append([])
        full_error.append([])
        for j in range(len(error[i])):
            if isnan(error[i,j]):
                pass
            else:
                dates_matrix[i].append(dates[i])
                full_error[i].append(error[i, j])

    for j in range(3):
            

        plt.close()

        # make individual plot
        fig = plt.figure(1)
        ax = fig.add_subplot(111)

        for i in range(len(dates_matrix)):
            if j == 0 and i == 0: 
                ax.scatter(dates_matrix[i], full_error[i], color='black', marker='o')
            elif j == 1 and (i == 0 or i == 1):
                ax.scatter(dates_matrix[i], full_error[i], color='black', marker='o')
            elif j == 2:
                ax.scatter(dates_matrix[i], full_error[i], color='black', marker='o')
            else:
                ax.scatter(dates_matrix[i], full_error[i], color='black', marker='')

        # set labels
        ax.set_xlabel(r'Date', fontsize=FONTSIZE)
        ax.set_ylabel(r'Normalised Error', fontsize=FONTSIZE)
        ax.set_title(title, fontsize=FONTSIZE)

        # edit axis ticks
        ax.xaxis.set_major_locator(days)
        ax.xaxis.set_major_formatter(monthsFmt)

        max_value = np.max(np.array(full_error))
        min_value = np.min(np.array(full_error))
        data_range = 0.05 * (max_value - min_value)
        data_range = 0.001
        ax.set_ylim([min_value - data_range, max_value + data_range])
        ax.set_xlim([dates_matrix[0][0] - 1, dates_matrix[-1][-1] + 1])

        ax.grid(b=True, which='major', linestyle='-.')
        fig.savefig('ensemble_scatter_'+str(variable)+'_'+str(j)+'_small.pdf',
                    orientation="landscape",
                    transparent=True,
                    bbox_inches='tight')
    
