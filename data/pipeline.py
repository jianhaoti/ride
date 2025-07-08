import pandas as pd
from config import analysis_config

class DataPipeline:
    def get_spatial_data(self):
        df = pd.read_csv(analysis_config.input_path, parse_dates=['Date/Time'])
        return df[['Lat', 'Lon']]
    
    def get_temporal_data(self):
        df = pd.read_csv(analysis_config.input_path, parse_dates=['Date/Time'])
        temporal_columns = ['Date/Time', 'Day Name', 'Is Weekend']

        return df[temporal_columns]
