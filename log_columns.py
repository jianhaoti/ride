import pandas as pd
import logging
from pathlib import Path

def log_unique_column_values(csv_file, inspect_column, log_dir='logs'):
    #log_dir is the directory where the log file will be saved

    Path(log_dir).mkdir(parents=True, exist_ok=True)

    #set up specific logger for this run

    logger = logging.getLogger(inspect_column)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_path = Path(log_dir) / f'{inspect_column}.log'
    file_handler = logging.FileHandler(log_path, mode='w')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    df = pd.read_csv(csv_file)

    unique_vals = df[inspect_column].unique()

    logger.info(f'Unique values in column {inspect_column}:')

    df = pd.read_csv(csv_file)

    if inspect_column not in df.columns:
        logger.error(f'Column {inspect_column} not found in the dataset')
        return


    unique_vals = df[inspect_column].dropna().unique()
    #dropna() is used to drop rows with missing values in the specified column

    logger.info(f'Unique values in column {inspect_column}:')
    for val in unique_vals:
        logger.info(f'{val}')

    logger.info(f'Total number of unique values: {len(unique_vals)}')


if __name__ == '__main__':
    log_unique_column_values('raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv', 'Facility Name')
    log_unique_column_values('raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv', 'Event Type')
