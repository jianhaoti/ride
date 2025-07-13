from numpy import concatenate
import pandas as pd
from config import data_paths_config as dp
from pathlib import Path
import glob 

def obtain_weather_columns(weather_df: pd.DataFrame):
    weather_columns = weather_df.columns
    file_name = "weather_columns.txt"
    output_file = Path(dp.weather_processed_path) / file_name
    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open(output_file, 'w') as f:
        for col in weather_columns:
            f.write(col + '\n')


def filter_out_weather_column_metadata(
    weather_columns_input_path=Path(dp.weather_processed_path) / "weather_columns.txt"
):
    delete_these_phrases = [
        "remarks", "wind_direction", "wind_gust", "wet_blub_temperature", "Measurement_Code", "Quality_Code", "Report_Type", "Source_Code", "station", "LATITUDE", "LONGITUDE", "Elevation", "precipitation_", "pressure_3hr_change", "altimeter", "sky_cover", "pres_"
    ]

    output_file = Path(dp.weather_processed_path) / "filtered_weather_columns.txt"
    with open(weather_columns_input_path, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not any(phrase.lower() in line.lower() for phrase in delete_these_phrases):
                outfile.write(line)

def filter_raw_weather_data(weather_path = dp.weather_raw_path):
    """"
    1. Group together raw weather data into processed_data/weather as sa csv
    2. Filter in only the columns in processsed_data/weather/filtered_weather_columns.txt
    3. Save to processsed_data/weather/filtered_weather_data.csv
    """

    ### 1 ###
    weather_path = Path(weather_path)
    all_weather_df = []

    for file_path in weather_path.glob("*.psv"):
        weather_df = pd.read_csv(file_path, sep = '|')
        all_weather_df.append(weather_df)

    for file_path in weather_path.glob("*.csv"):
        weather_df = pd.read_csv(file_path)
        all_weather_df.append(weather_df)
    
    combined_df = pd.concat(all_weather_df)
    combined_df['DATE'] = pd.to_datetime(combined_df['DATE'])
    combined_df.to_csv(Path(dp.weather_processed_path) / "weather.csv", index=False)
    
    ### 2 ###
    filter_in_these_cols = []
    with open(Path(dp.weather_processed_path) / "filtered_weather_columns.txt", 'r') as f:
        for line in f:
            filter_in_these_cols.append(line.strip())
    
    combined_df = combined_df[filter_in_these_cols]
    
    ### 3 ###
    combined_df.to_csv(Path(dp.weather_processed_path) / "filtered_weather.csv", index=False)
    


    
    pass