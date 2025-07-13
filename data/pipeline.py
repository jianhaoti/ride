import pandas as pd
from config import data_paths_config as dp

class DataPipeline:
    def get_spatial_data(self):
        df = pd.read_csv(dp.uber_processed_csv, parse_dates=['Date/Time'])
        return df[['Lat', 'Lon']]
    
    def get_temporal_data(self):
        df = pd.read_csv(dp.uber_processed_csv, parse_dates=['Date/Time'])
        temporal_columns = ['Date/Time', 'Day Name', 'Is Weekend']

        return df[temporal_columns]

    def get_weather_data(self):
        df = pd.read_csv(dp.weather_raw_psv, sep = '|')
        return df