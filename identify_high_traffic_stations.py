import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
from matplotlib.ticker import ScalarFormatter

%config InlineBackend.figure_format = 'svg'
%matplotlib inline

"""
Based on borough EDA, top boroughs for marketing teams targeting
women in technology are below in order.

1. Manhattan
2. Brooklyn
3. Queens

Subway stations will be selected based on EDA below
and on the borough priorities above.
"""

def import_data():
    mta_daily = pd.read_csv('mta_daily.csv')
    mta_hourly = pd.read_csv('mta_hourly.csv')
    return mta_daily, mta_hourly

mta_daily, mta_hourly = import_data()

def peak_stations(data, borough):
    """Takes in a dataset and borough and identifies top subway stations in that borough."""
    # identify total entries per station per week
    weekly_sta_entries = data.groupby(['station','borough', data.datetime.dt.week])['daily_entries'].agg([np.sum]).reset_index()
    weekly_sta_entries = weekly_sta_entries.rename(columns={'datetime': 'week', 'sum':'weekly_entries'})

    # identify mean weekly entries per station
    mean_weekly_entries = weekly_sta_entries.groupby(['station', 'borough'])['weekly_entries'].agg(['mean'])
    mean_weekly_entries = mean_weekly_entries.rename(columns = {'mean': 'mean_weekly_entries'})


    top_stations = mean_weekly_entries[mean_weekly_entries.borough==borough_name].sort_values(by='mean_weekly_entries', ascending=False)[:10]
    top_sta_list = [sta for sta in top_stations.station]

    return top_sta_list

top_bk = peak_stations(mta_daily, 'Bk')[1:2] #row zero is an error due to matching station names in manhattan and brooklyn. Removed after outside research.
top_bk = peak_stations(mta_daily, 'M')[:7]
top_q = peak_stations(mta_daily, 'Q')[:2]

all_top_sta = top_bk + top_m + top_q

# Plot daily traffic for top trains for April only to more cleanly visualize patterns
daily_station_entries = mta_daily.groupby('station')['daily_entries'].agg(['mean'])

plt.figure(figsize=(14,5))

for sta in all_top_sta:
    single_station = grouped_by_station_and_day[grouped_by_station_and_day.station == sta]
    ss_boundary = single_station[(single_station.date >= pd.to_datetime('2019-04-1').date()) & (single_station.date <= pd.to_datetime('2019-04-29').date())]
    time_plot = sns.lineplot(x=ss_boundary.date, y = ss_boundary.daily_entries, label=sta);

time_plot.legend(loc=3, fontsize='10', shadow=True);
time_plot.set_title('Determing High Traffic Stations By Daily Traffic', fontsize=12)
time_plot.set_ylabel('Daily Entries', fontsize=12)
time_plot.set_xlabel('Date', fontsize=12);
sns.despine()
sns.set_style('white')
sns.set_palette("Set2");

plt.savefig("Apr_Determing_high_traffic_stations_by_daily_traffic.png")

#Identify traffic by day of week for the top stations to determine optimal street team posting dates
grp_by_sta_dow = mta_daily.groupby(['station', 'dow', 'dow_num'])['daily_entries'].agg([np.mean]).reset_index()
grp_by_sta_dow = grp_by_sta_dow.rename(columns={'mean': 'mean_dow_entries'})

plt.figure(figsize=(12,5))

days = ['','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
for sta in all_top_sta:
    single_station = grp_by_sta_dow[grp_by_sta_dow.station == sta].sort_values(by='dow_num')
    dow_plot = sns.lineplot(x=single_station.dow_num, y = single_station.mean_dow_entries, label=sta);

dow_plot.legend(fontsize='10', shadow=True, loc=3);
dow_plot.set_title('Top Station Traffic by Day of the Week', fontsize=14)
dow_plot.set_ylabel('Mean Daily Entries', fontsize=12)
dow_plot.set_xlabel('Day of Week', fontsize=12);
dow_plot.set_xticklabels(labels=days)

sns.despine()
sns.set_style('white')
sns.set_palette("Set2");

plt.savefig("Top_station_traffic_by_day_of_week.png")
