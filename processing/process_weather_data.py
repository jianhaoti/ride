import pandas as pd
from config import data_paths_config as dp
from pathlib import Path

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
        "Measurement_Code", "Quality_Code", "Report_Type", "Source_Code", "Source_Station_ID"
    ]
    output_file = Path(dp.weather_processed_path) / "filtered_weather_columns.txt"
    with open(weather_columns_input_path, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not any(phrase in line for phrase in delete_these_phrases):
                outfile.write(line)