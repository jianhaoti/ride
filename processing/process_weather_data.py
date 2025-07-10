import pandas as pd

def obtain_weather_columns(weather_df: pd.DataFrame, output_path: str):
    weather_columns = weather_df.columns
    
    with open(f'{output_path}', 'w') as f:
        for col in weather_columns:
            f.write(col)


def filter_out_weather_column_metadata(weather_columns_input_path: str, output_path: str):
    delete_these_phrases = ["Measurement_Code", "Quality_Code", "Report_Type", "Source_Code", "Source_Station_ID"]
    lines = []
    filtered_lines = []

    with open(f'{weather_columns_input_path}', 'r') as f:
        for line in f:
            lines.append(line)
    
    for line in lines:
        if not any(phrase in line for phrase in delete_these_phrases):
            filtered_lines.append(line)
        
    
    with open(f'{output_path}', 'w') as f:
        for line in filtered_lines:
            f.write(line)