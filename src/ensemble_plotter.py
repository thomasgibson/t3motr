from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt
import time
import datetime

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

print('blah')

variables = ['pressure_error', 'temperature_error', 'rainfall_error']
labels1 = ['Normalised Pressure Error', 'Normalised Temperature Error', 'Normalised Rainfall Error']
labels2 = ['Mean pressure error', 'Mean temperature error', 'mean rainfall error']

dates_raw = data.variables['date']
dates = []

# convert dates
for i in range(len(dates_raw[:])):
    year, month, day = convert_date(dates_raw[i])
    dt = datetime.datetime(year=year, month=month, day=day)
    dates.append(time.mktime(dt.timetuple()))


for variable, label1, label2 in zip(variables, labels1, labels2):

    error = data.variables[variable][:,:]
    full_dates = []
    full_error = []
    mean_error = []

    for i in range(len(error)):
        mean_error.append(np.mean(error[i]))
        for j in range(len(error[i])):
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

    ax.scatter(full_dates, full_error, color='black', marker='o')
    ax.set_xlabel(r'Date', fontsize=28)
    ax.set_ylabel(label1, fontsize=28)

    fig.savefig('ensemble_scatter_'+str(variable)+'.pdf')

    plt.close()

    # declare font properties for figure
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    font = {'size':28}
    plt.rc('font',**font)

    # make individual plot
    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    ax.scatter(dates, mean_error, color='black', marker='o')
    ax.set_xlabel(r'Date', fontsize=28)
    ax.set_ylabel(label2, fontsize=28)

    fig.savefig('ensemble_mean_error_'+str(variable)+'.pdf')
    
