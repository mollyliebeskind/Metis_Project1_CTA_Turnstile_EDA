import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

"""
This file does four tasks.
1. imports and cleans MTA turnstyle data
2. Imports and cleans MTA subway location data
3. Merges the two datasets and saves the ouput as a csv file
4. Engineers new features and a daily + hourly datset and saves outputs to a csv
"""

# Task 1: import and clean MTA turnstyle data
def all_saturdays(start_date, end_date):
    """ Takes two dates and returns a list of saturdays between the first date and a week after the second date"""

    modified_end_date = datetime.datetime.strptime(end_date,'%m/%d/%Y') + datetime.timedelta(weeks = 1)
    saturday_list = pd.date_range(start=start_date, end=modified_end_date,
                              freq='W-SAT').strftime('%m/%d/%Y').tolist()
    return saturday_list

def import_mta(date):
    """reads in MTA turnstile data published online for a given date"""

    formatted_date = date[-2:]+date[:2]+date[3:5]
    base_url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt"
    date_url = base_url.format(formatted_date)
    date_data = pd.read_csv(date_url)
    return date_data

def mta_to_df(saturday_list):
    """imports MTA turnstile data for a list of dates and then concatenates them"""

    dict_of_dfs = {}
    for saturday in saturday_list:
        dict_of_dfs[saturday] = pd.DataFrame(import_mta(saturday))
    mta = pd.DataFrame()
    for val in dict_of_dfs.values():
        mta = pd.concat([mta, val])
    return mta

def import_data():
    start_date = input("Enter start date (X/X/XXXX): ")
    end_date = input("Enter end date (X/X/XXXX): ")

    saturday_list = all_saturdays(start_date,end_date)
    mta_df = mta_to_df(saturday_list)

    # to keep only the specified dates rather than saturday-saturday
    mta_df.DATE = pd.to_datetime(mta_df.DATE,format="%m/%d/%Y")
    mta_df = mta[(mta.DATE >= start_date)]

    return mta_df

def basic_df_cleaning(data):
    """
    Replaces all column names with lower case and removes spaces and / symbols.
    Combines date and time columns into a single datetime column.
    """

    data.columns = data.columns.str.strip().str.lower().str.replace('/',"_")
    data["datetime"] = pd.to_datetime(data.date + " " + data.time, format="%m/%d/%Y %H:%M:%S")
    data = data.drop(columns = ['time']) # replaced with datetime above

    return data

def remove_duplicates(data):
    """Takes in a dataset and identifies then drops all duplicate rows."""

    before_duplicates = data.duplicated(subset=["c_a", "unit", "scp", "station", "datetime"]).sum()
    print(f"There are {before_duplicates} duplicates in the dataset.")

    data = data.drop_duplicates(subset=["c_a", "unit", "scp", "station", "datetime"])

    after_duplicates = data.duplicated(subset=["c_a", "unit", "scp", "station", "datetime"]).sum()
    print(f"All duplicates dropped. There are now {after_duplicates} duplicates in the dataset.")

    return data

mta = import_data()
mta = basic_df_cleaning(mta)
mta = remove_duplicates(mta)

# Task 2: import and clean MTA subway location data
def import_location_data():
    return pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')


def clean_location_data(data):
    data.columns = data.columns.str.strip().str.lower().str.replace('/',"_").str.replace(' ', '_')
    data['stop_name'] = data.stop_name.str.upper().str.strip()

    return data

locations = import_location_data()
locations = clean_location_data(locations)

# Task 3: Merge the two datasets and save the ouput as a csv file

#several of the names in the datasets are not consistent. Adjustments are made to the datasets prior to merging.
#replace the string naming of location.stop_name to match that of mta.station

mta = mta['station'].replace({"4AV-9 ST":"4 AV-9 ST",
                               'TWENTY THIRD ST':'23 ST',
                               'THIRTY THIRD ST':'33 ST'}
                              )

#replace the string naming of location.stop_name to match that of mta.station
locations = locations['stop_name'].replace({" - ":"-",
                                            "CENTER":"CTR",
                                            "SQ-E TREMONT AV":"SQ",
                                            " UNIVERSITY":"",
                                            "PLAZA":"PZ",
                                            "COLLEGE":"COL",
                                            "STATION":"STA",
                                                 },
                                                     regex=True)

#replace the string naming of location.stop_name to match that of mta.station
locations = locations['stop_name'].replace({"103 ST-CORONA PZ":"103 ST-CORONA",
                                            "137 ST-CITY COL":"137 ST CITY COL",
                                            "138 ST-GRAND CONCOURSE":"138/GRAND CONC",
                                            "149 ST-GRAND CONCOURSE":"149/GRAND CONC",
                                            "15 ST-PROSPECT PK":"15 ST-PROSPECT",
                                            "161 ST-YANKEE STADIUM":"161/YANKEE STAD",
                                            "163 ST-AMSTERDAM AV":"163 ST-AMSTERDM",
                                            "21 ST-QUEENSBRIDGE":"21 ST-QNSBRIDGE",
                                            "3 AV-138 ST":"3 AV 138 ST",
                                            "40 ST":"40 ST LOWERY ST",
                                            "42 ST-PORT AUTHORITY BUS TERMINAL":"42 ST-PORT AUTH",
                                            "5 AV":"5 AVE",
                                            "59 ST-COLUMBUS CIRCLE":"59 ST COLUMBUS",
                                            "66 ST-LINCOLN CTR":"66 ST-LINCOLN",
                                            "68 ST-HUNTER COL":"68ST-HUNTER CO",
                                            "75 ST":"75 ST-ELDERTS",
                                            "81 ST-MUSEUM OF NATURAL HISTORY":"81 ST-MUSEUM",
                                            "82 ST-JACKSON HTS":"82 ST-JACKSON H",
                                            "85 ST-FOREST PKWY":"85 ST-FOREST PK",
                                            "90 ST-ELMHURST AV":"90 ST-ELMHURST",
                                            "9 ST":"9TH STREET",
                                            "AQUEDUCT-N CONDUIT AV":"AQUEDUCT N.COND",
                                            "AQUEDUCT RACETRACK":"AQUEDUCT RACETR",
                                            "ASTORIA-DITMARS BLVD":"ASTORIA DITMARS",
                                             'ATLANTIC AV-BARCLAYS CTR':'ATL AV-BARCLAY',
                                             'BEDFORD-NOSTRAND AVS':'BEDFORD-NOSTRAN',
                                             'BEVERLEY RD':'BEVERLEY ROAD',
                                             'BRIARWOOD-VAN WYCK BLVD':'BRIARWOOD',
                                             'BROADWAY-LAFAYETTE ST':"B'WAY-LAFAYETTE",
                                             '15 ST-PROSPECT PARK':'15 ST-PROSPECT',
                                             '47-50 STS CTR':'47-50 STS ROCK',
                                             'BEDFORD PARK BLVD':'BEDFORD PK BLVD',
                                             'BROOKLYN BRIDGE-CITY HALL':'BROOKLYN BRIDGE',
                                             'BUSHWICK AV-ABERDEEN ST':'BUSHWICK AV',
                                             'CANARSIE-ROCKAWAY PKWY':'CANARSIE-ROCKAW',
                                             'CENTRAL PARK NORTH (110 ST)':'CENTRAL PK N110',
                                             'CHRISTOPHER ST-SHERIDAN SQ':'CHRISTOPHER ST',
                                             'CLINTON-WASHINGTON AVS':'CLINTON-WASH AV',
                                             'CONEY ISLAND-STILLWELL AV':'CONEY IS-STILLW',
                                             'COURT ST':'COURT SQ-23 ST',
                                             'CROWN HTS-UTICA AV':'CROWN HTS-UTICA',
                                             'DELANCEY ST':'CROWN HTS-UTICA',
                                             'E 105 ST':'EAST 105 ST',
                                             "E 143 ST-ST MARY'S ST":"E 143/ST MARY'S",
                                             'EASTCHESTER-DYRE AV':'EASTCHSTER/DYRE',
                                             'EASTERN PKWY-BROOKLYN MUSEUM':'EASTN PKWY-MUSM',
                                             'FAR ROCKAWAY-MOTT AV': 'FAR ROCKAWAY',
                                             'FLATBUSH AV-BROOKLYN COL':'FLATBUSH AV-B.C',
                                             'FLUSHING-MAIN ST':'FLUSHING-MAIN',
                                             'FOREST AV':'FOREST AVE',
                                             'FOREST HILLS-71 AV':'FOREST HILLS 71',
                                             'FORT HAMILTON PKWY': 'FT HAMILTON PKY',
                                             'GRAND ARMY PZ':'GRAND ARMY PLAZ',
                                             'GRAND AV-NEWTOWN':'GRAND-NEWTOWN',
                                             'GRAND CENTRAL-42 ST':'GRD CNTRL-42 ST',
                                             'HARLEM-148 ST':'HARLEM 148 ST',
                                             'HOWARD BEACH-JFK AIRPORT':'HOWARD BCH JFK',
                                             'HOYT-SCHERMERHORN STS':'HOYT-SCHER',
                                             'HUNTERS POINT AV':'HUNTERS PT AV',
                                             'JAMAICA CTR-PARSONS/ARCHER':'JAMAICA CENTER',
                                             'JAMAICA-179 ST':'JAMAICA 179 ST',
                                             'JAMAICA-VAN WYCK':'JAMAICA VAN WK',
                                             'JAY ST-METROTECH':'JAY ST-METROTEC',
                                             'KEW GARDENS-UNION TPKE':'KEW GARDENS',
                                             'KINGSTON-THROOP AVS':'KINGSTON-THROOP',
                                             'KNICKERBOCKER AV':'KNICKERBOCKER',
                                             'LEXINGTON AV/53 ST':'LEXINGTON AV/53',
                                             'LEXINGTON AV/63 ST':'LEXINGTON AV/63',
                                             'MARBLE HILL-225 ST':'MARBLE HILL-225',
                                             'METS-WILLETS POINT':'METS-WILLETS PT',
                                             'MORRISON AV- SOUND VIEW':'MORISN AV/SNDVW',
                                             'MYRTLE-WILLOUGHBY AVS': 'MYRTLE-WILLOUGH',
                                             'MYRTLE-WYCKOFF AVS':'MYRTLE-WYCKOFF',
                                             'NORWOOD-205 ST': 'NORWOOD 205 ST',
                                             'OZONE PARK-LEFFERTS BLVD':'OZONE PK LEFFRT',
                                             'PARK PL': 'PARK PLACE',
                                             'QUEENS PZ':'QUEENS PLAZA',
                                             'ROCKAWAY PARK-BEACH 116 ST':'ROCKAWAY PARK B',
                                             'ROOSEVELT ISLAND':'ROOSEVELT ISLND',
                                             'SENECA AV':'SENECA AVE',
                                             'SMITH-9 STS':'SMITH-9 ST',
                                             'ST GEORGE':'ST. GEORGE',
                                             'VAN CORTLANDT PARK-242 ST':'V.CORTLANDT PK',
                                             'VERNON BLVD-JACKSON AV':'VERNON-JACKSON',
                                             'W 4 ST':'W 4 ST-WASH SQ',
                                             'W 8 ST-NY AQUARIUM':'W 8 ST-AQUARIUM',
                                             'WAKEFIELD-241 ST':'WAKEFIELD/241',
                                             'WTC CORTLANDT':'WTC-CORTLANDT',
                                             '4 AV':'4 AV-9 ST',
                                             'ESSEX ST':'DELANCEY/ESSEX',
                                             'JACKSON HTS-ROOSEVELT AV':'JKSN HT-ROOSVLT',
                                             'NEWKIRK PZ':'NEWKIRK PLAZA',
                                             'QUEENSBORO PZ':'QUEENSBORO PLZ',
                                             'SUTPHIN BLVD-ARCHER AV-JFK AIRPORT':'SUTPHIN-ARCHER',
                                             'SUTTER AV-RUTLAND RD':'SUTTER AV-RUTLD',
                                             'UNION SQ-14 ST':'14TH STREET',
                                             'WHITEHALL ST':'WHITEHALL S-FRY',
                                             'WOODSIDE-61 ST':'61 ST WOODSIDE',
                                            '34 ST-11 AV':'34 ST-HUDSON YD',
                                            'JAMAICA CTR':'JAMAICA CENTER',
                                            '47-50 STS-ROCKEFELLER CTR':'47-50 STS ROCK',
                                            'WEST FARMS SQ-E TREMONT AV':'WEST FARMS SQ',
                                             'WESTCHESTER SQ-E TREMONT AV':'WESTCHESTER SQ'
                                           })

mta_locations = mta.merge(locations, left_on=['station', 'division'], right_on=['stop_name', 'division'], suffixes=('_left', '_right'))

#Save file as csv to reference later if needed
mta_locations.to_csv(r'mta_locations.csv')

# Task 4: engineer new features and daily + hourly Datasets

def prepare_daily_dataset(data):

    #to obtain daily entries, isolate a single reading per day
    daily = data.groupby(['c_a', 'unit', 'scp', 'station', 'borough', data.datetime.dt.date])['entries'].min().reset_index()

    #add a column that calculates daily entries as the difference between entry total from day n and n+1
    daily['daily_entries'] = daily.groupby(['c_a', 'unit', 'scp', 'station'])['entries'].diff().shift(-1)

    #remove impossible entry values and outliers caused by system reboot that happens randomly
    daily = daily[daily.daily_entries >= 0]
    daily = daily[daily.daily_entries < daily.daily_entries.quantile(q =.997)]

    #create columns that indicate day of week and number of day of the week
    daily.datetime = pd.to_datetime(daily.datetime,format="%Y/%m/%d")
    daily['dow'] = daily.datetime.dt.day_name()
    daily['dow_num'] = daily.datetime.dt.dayofweek

    return daily

def prepare_hourly_dataset(data):
    hourly = mta_locations.groupby(['c_a', 'unit', 'scp', 'station', mta_locations.datetime]).min().reset_index()

    hourly['y_entries'] = hourly.entries.shift(1) #helper column to calculate hourly difference
    hourly['hourly_entries'] = hourly.entries - hourly.y_entries

    #remove impossible entry values and outliers caused by system reboot that happens randomly
    hourly = hourly[hourly.hourly_entries >= 0]
    hourly = hourly[hourly.hourly_entries < hourly.hourly_entries.quantile(q =.99)]

    #create columns that indicate day of week
    hourly['dow'] = hourly.datetime.dt.day_name()

    return hourly

mta_daily = prepare_daily_dataset(mta_locations)
mta_hourly = prepare_hourly_dataset(mta_locations)

mta_daily.to_csv(r'mta_daily.csv')
mta_hourly.to_csv(r'mta_hourly.csv')
