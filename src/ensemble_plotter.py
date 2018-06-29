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
labels1 = ['Normalised Pressure Error', 'Normalised Rainfall Error']
labels2 = ['Mean pressure error', 'mean rainfall error']

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


for variable, label1, label2 in zip(variables, labels1, labels2):

    error = data.variables[variable][:,:]
    full_dates = []
    full_error = []
    mean_error = []

    for i in range(len(error)):
        mean_error.append(np.mean(error[i]))
        for j in range(len(error[i])):
            if isnan(error[i,j]):
                pass
            else:
                full_dates.append(dates[i])
                full_error.append(error[i, j])
            

    plt.close()
    # declare font properties for figure
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    font = {'size':28}
    plt.rc('font',**font)

    # make individual plot
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    ax.scatter(full_dates, full_error, color='black', marker='.', s=0.2)
    ax.set_xlabel(r'Date', fontsize=24)
    ax.set_ylabel(label1, fontsize=24)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    data_range = 0.05 * (np.max(full_error) - np.min(full_error))
    ax.set_ylim([np.min(full_error) - data_range, np.max(full_error) + data_range]) 
    
    fig.savefig('ensemble_scatter_'+str(variable)+'.pdf', bbox_inches='tight')

    plt.close()

    # declare font properties for figure
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    font = {'size':28}
    plt.rc('font',**font)

    # make individual plot
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    ax.plot(dates, mean_error, color='black', marker='', linestyle='-')
    ax.set_xlabel(r'Date', fontsize=24)
    ax.set_ylabel(label2, fontsize=24)

    fig.savefig('ensemble_mean_error_'+str(variable)+'.pdf', bbox_inches='tight')
    
