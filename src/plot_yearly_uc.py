import numpy as np
import netCDF4 as nc
import sys
import matplotlib.pyplot as plt
import seaborn as sns

from collections import defaultdict

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


FONTSIZE = 12
MARKERSIZE = 10
LINEWIDTH = 3


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


def organize_data(data_set):

    dates = data_set['date']
    pr_err = np.asarray(data_set['pressure_error'][:]).tolist()
    t_err = np.asarray(data_set['temperature_error'][:]).tolist()
    rain_err = np.asarray(data_set['rainfall_error'][:]).tolist()

    data = AutoVivification()
    start_idx = AutoVivification()

    for i, date in enumerate(dates):
        year, month, day = convert_date(date)

        if not bool(start_idx[year][month]) and start_idx[year][month] != 0:
            start_idx[year][month] = i

        data[year][month][day]["pressure_error"] = pr_err[i]
        data[year][month][day]["temperature_error"] = t_err[i]
        data[year][month][day]["rainfall_error"] = rain_err[i]

    return data, start_idx

data, start_idx = organize_data(data_set)
        
yearly_pr_err = defaultdict(list)
yearly_t_err = defaultdict(list)
yearly_rain_err = defaultdict(list)
yearly_month_idx = AutoVivification()

for year in data:
    for month in data[year]:
        # Always start at 0 for Jan.
        yearly_month_idx[year][month] = start_idx[year][month] - start_idx[year][1]

        for day in data[year][month]:

            yearly_pr_err[year].append(data[year][month][day]["pressure_error"])
            yearly_t_err[year].append(data[year][month][day]["temperature_error"])
            yearly_rain_err[year].append(data[year][month][day]["rainfall_error"])

month_mapper = {1: "Jan.",
                2: "Feb.",
                3: "Mar.",
                4: "Apr.",
                5: "May",
                6: "Jun.",
                7: "Jul.",
                8: "Aug.",
                9: "Sep.",
                10: "Oct.",
                11: "Nov.",
                12: "Dec."}

fig, axes = plt.subplots(4, 1, figsize=(12, 3), squeeze=False)
axes = axes.flatten()
ax1, ax2, ax3, ax4 = axes

for ax in axes:
    ax.set_ylabel("Normalized Error", fontsize=FONTSIZE)

ax_mapper = {2013: ax1,
             2014: ax2,
             2015: ax3,
             2016: ax4}

for year in yearly_pr_err:

    ax = ax_mapper[year]
    pr = yearly_pr_err[year]
    t = yearly_t_err[year]
    rain = yearly_rain_err[year]

    idx = yearly_month_idx[year]
    idx_vals = list(idx.values())

    ax.plot(list(range(len(pr))), pr, label="Pressure UC")
    # ax.plot(list(range(len(t))), t, label="Temp. UC")
    # ax.plot(list(range(len(rain))), rain, label="Rainfall UC")

    ax.set_xticks(idx_vals)
    ax.set_xticklabels(list(month_mapper.values()))

sns.despine(fig)
fig.savefig("yearly_uc.pdf",
            orientation="landscape",
            format="pdf",
            transparent=True,
            bbox_inches="tight")
