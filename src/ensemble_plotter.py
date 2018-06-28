from netCDF4 import Dataset
import numpy as np
from matplotlib import rc
import matplotlib.pyplot as plt

data = Dataset('ensemble_spread.nc', 'r')

variables = ['pressure_error', 'temperature_error', 'rainfall_error']
labels1 = ['Normalised Pressure Error', 'Normalised Temperature Error', 'Normalised Rainfall Error']
labels2 = ['Mean pressure error', 'Mean temperature error', 'mean rainfall error']

dates_raw = data.variables['date']
dates = date_convert(dates_raw)

for variable, label1, label2 in zip(variables, labels1, labels2):

    error = data.variables['variable'][:,:]
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
    ax.set_ylabel(label, fontsize=28)

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
    ax.set_ylabel(label, fontsize=28)

    fig.savefig('ensemble_mean_error_'+str(variable)+'.pdf')
    
