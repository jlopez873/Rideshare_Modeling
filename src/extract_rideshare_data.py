import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
pd.set_option('mode.chained_assignment', None)

def clean_tripdata(years):
    
    taxi_zones = pd.read_csv('data/taxi_zones.csv')
    taxi_zones.columns = [taxi_zones[col].name.lower() for col in taxi_zones]
    taxi_zones = taxi_zones[['locationid', 'borough']]
    
    # Load tripdata files
    def load_df(year):
        files_dict = {}
        for root, dirs, files in os.walk('./data/rideshare_data/'+year, topdown=False):
            for name in files:
                filename = name[6:22].replace('-', '_')
                files_dict[filename] = pd.read_parquet(os.path.join(root, name))
                print(filename, 'loaded')
        print('all', year, 'files loaded')
        return files_dict
    
    
    # Define dataframe cleaning helper function
    def clean_df(df):
        # Set index to pickup datetime
        df.set_index('pickup_datetime', drop=True, inplace=True)
        df.index.name = None

        # Make all columns lowercase
        df.columns = [df[col].name.lower() for col in df.columns]

        # Keep only study columns
        df = df[['hvfhs_license_num', 'pulocationid']]

        # Split by provider
        uber = df[['pulocationid']][df.hvfhs_license_num == 'HV0003']
        lyft = df[['pulocationid']][df.hvfhs_license_num == 'HV0005']
        del df
        
        # Merge tripdata with taxi zones
        uber_index = uber.index
        lyft_index = lyft.index
        uber, lyft = [df.merge(taxi_zones, left_on='pulocationid', right_on='locationid') for df in [uber, lyft]]
        uber.index = uber_index
        lyft.index = lyft_index

        # Remove taxi zone columns
        [df.drop(['pulocationid', 'locationid'], axis=1, inplace=True) for df in [uber, lyft]]

        # Create dummy variables for boroughs
        uber, lyft = [pd.concat([df, pd.get_dummies(df.borough)], axis=1) for df in [uber, lyft]]

        # Drop non-borough columns
        [df.drop('borough', axis=1, inplace=True) for df in [uber, lyft]]
        if 'EWR' in uber.columns:
            uber.drop('EWR', axis=1, inplace=True)
        if 'EWR' in lyft.columns:
            lyft.drop('EWR', axis=1, inplace=True)
        if 'Unknown' in uber.columns:
            uber.drop('Unknown', axis=1, inplace=True)
        if 'Unknown' in lyft.columns:
            lyft.drop('Unknown', axis=1, inplace=True)

        # Standardize column names
        uber.columns, lyft.columns = [[col.lower().replace(' ', '_') for col in df.columns] for df in [uber, lyft]]

        # Aggregate tripdata by day
        uber_rides, lyft_rides = [df.resample('D').agg(
            {'bronx':'sum', 'brooklyn':'sum', 'manhattan':'sum', 'queens':'sum', 'staten_island':'sum'}
        ) for df in [uber, lyft]]
        del uber, lyft
        
        # Create citywide total column
        uber_rides['nyc'], lyft_rides['nyc'] = [df.sum(axis=1) for df in [uber_rides, lyft_rides]]

        return uber_rides, lyft_rides
    
    # Define function to concatenate monthly dataframes into year dataframe
    def concat_dfs(rides_dict):
        data = pd.DataFrame()
        for key, value in rides_dict.items():
            data = pd.concat([data, value])
        return data
    
    annual_rides_uber = {}
    annual_rides_lyft = {}
    
    for year in years:
        # Load tripdata
        df_dict = load_df(year)
    
        # Create dictionary of clean dataframes
        uber_dict = {}
        lyft_dict = {}
    
        # Clean dataframes and insert into dictionary
        for key, value in df_dict.items():
            uber_dict[key], lyft_dict[key] = clean_df(value)
    
        annual_rides_uber[year], annual_rides_lyft[year] = [
            concat_dfs(rides_dict) for rides_dict in [uber_dict, lyft_dict]]
        del uber_dict, lyft_dict
        
    uber, lyft = [concat_dfs(annual_rides_dict) for annual_rides_dict in [annual_rides_uber, annual_rides_lyft]]
    del annual_rides_uber, annual_rides_lyft
    
    [df.sort_index(inplace=True) for df in [uber, lyft]]
    
    uber.to_parquet('data/clean_uber_tripdata.parquet')
    lyft.to_parquet('data/clean_lyft_tripdata.parquet')
    print('Data cleaning completed.')
    
def main():
    clean_tripdata(['2019', '2020', '2021', '2022'])
    
if __name__ == '__main__':
    main()