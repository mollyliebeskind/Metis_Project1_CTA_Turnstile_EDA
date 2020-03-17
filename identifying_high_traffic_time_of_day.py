import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
from matplotlib.ticker import ScalarFormatter

%config InlineBackend.figure_format = 'svg'
%matplotlib inline

"""
This file identifies the best time of day to deploy marketing teams to NYC Subway
stations that were identified to have the highest traffic.

Note:
Due to day light savings, some of the data has recordings at hours 0,4,8,12,16,20,24
while other data has recordings at hours 0,3,7,11,15,19,23. This error causes various
recordings to occur between the standard 4 hour increments. To account for hourly
variations and daylight savings, grouping hourly data into 3 hour increments
"""

def import_data():
    mta_daily = pd.read_csv('mta_daily.csv')
    mta_hourly = pd.read_csv('mta_hourly.csv')
    return mta_daily, mta_hourly

def top_station_dataset(data, list_of_stop_stations):
    """Reduces dataset to only the top stations to decrease computation and time needed for executions."""
    x1, x2, x3, x4, x5, x6, x7, x8, x9 = list_of_stop_stations

    all_days_top_sta = mta_hourly[(mta_hourly.station == x1) |
                                  (mta_hourly.station == x2) |
                                  (mta_hourly.station == x3) |
                                  (mta_hourly.station == x4) |
                                  (mta_hourly.station == x5) |
                                  (mta_hourly.station == x6) |
                                  (mta_hourly.station == x7) |
                                  (mta_hourly.station == x8) |
                                  (mta_hourly.station == x9)
                                 ]
    return all_days_top_sta

def define_hour_groups(data):
    for row in data.index:
        if data.loc[row, 'datetime'] == 0:
            data.loc[row, 'hour_group'] = 0
        elif 0 < data.loc[row, 'datetime'] <= 3:
            data.loc[row, 'hour_group'] = 3
        elif 3 < data.loc[row, 'datetime']  <= 6:
            data.loc[row, 'hour_group'] = 6
        elif 6 < data.loc[row, 'datetime']  <= 9:
            data.loc[row, 'hour_group'] = 9
        elif 9 < data.loc[row, 'datetime']  <= 12:
            data.loc[row, 'hour_group'] = 12
        elif 12 < data.loc[row, 'datetime'] <= 15:
            data.loc[row, 'hour_group'] = 15
        elif 15 < data.loc[row, 'datetime']  <= 18:
            data.loc[row, 'hour_group'] = 18
        elif 18 < data.loc[row, 'datetime'] <= 21:
            data.loc[row, 'hour_group'] = 21
        elif 21 < data.loc[row, 'datetime'] <= 24:
            data.loc[row, 'hour_group'] = 24
    return data

def entries_per_hour_block(data, top_stations_list):
    """
    Calls helper functions to isolate the dataset to only top stations,
    group the data into 3 hour blocks of time and compute entries within those hourly times.
    Returns a dataset grouped by time block.
    """

    #isolate dataset to only the top stations
    all_days_top_sta = top_station_dataset(mta_hourly, all_top_sta)

    hourly_dow = all_days_top_sta.groupby(['dow', all_days_top_sta.datetime.dt.hour])['hourly_entries'].agg(['mean']).reset_index()
    hourly_dow = hourly_dow.rename(columns={'mean':'hourly_mean'})

    # create hour blocks
    hourly_dow = define_hour_groups(hourly_dow)

    # compute entries within hourly blocks
    grp_hourly_dow = hourly_dow.groupby(['dow', 'hour_group'])['hourly_mean'].agg(['sum']).reset_index()
    grp_hourly_dow = grp_hourly_dow.rename(columns = {'sum': 'entries_per_hour_group'})

    return grp_hourly_dow

mta_daily, mta_hourly = import_data()
grp_hourly_dow = entries_per_hour_block(all_days_top_sta)

#plot hourly traffic for the busiest days of the week to determine posting times
days = ['Tuesday', 'Wednesday', 'Thursday', 'Friday']
peak_days = grp_hourly_dow[(grp_hourly_dow.dow == 'Tuesday') |
                       (grp_hourly_dow.dow == 'Wednesday') |
                       (grp_hourly_dow.dow == 'Thursday') |
                       (grp_hourly_dow.dow == 'Friday')
                      ]
plt.figure(figsize=(10,4))
bar_time = sns.barplot(x=peak_days.hour_group, y = peak_days.entries_per_hour_group, hue=peak_days.dow);


bar_time.legend(fontsize='10', loc=2)
bar_time.set_title('High Traffic Station Activity')
bar_time.set_ylabel('Mean Entries Per 3 Hour Block')
bar_time.set_xlabel('Ending Hour of 3-Hour Block')
plt.savefig("Station_Traffic_By_Hour.png")
sns.set_palette("Set2")
sns.despine()

plt.savefig("Peak_days_Station_Traffic_By_Hour.png")

# Plotting for only Friday for sipmle visualization
thursday_hours = grp_hourly_dow[(grp_hourly_dow.dow == 'Thursday')]
plt.figure(figsize=(10,4))
bar_time = sns.barplot(x=single_day.hour_group, y = single_day.entries_per_hour_group, color='#042263FF');


bar_time.set_title('Thursday Station Traffic By Hour')
bar_time.set_ylabel('Mean Hourly Entries')
bar_time.set_xlabel('Hour of The Day')
sns.despine()

plt.savefig("Thursday_Station_Traffic_By_Hour.png")
