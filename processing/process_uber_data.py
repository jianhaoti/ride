import pandas as pd
import zipfile
import glob
from pathlib import Path
from config import data_paths_config

def process_uber_data() -> pd.DataFrame:
    """
    1. take all the zipped files in the raw_data directory
    2. unzip files into the /data 
    3. combine files into a single dataframe
    4. return the dataframe into processed_data/combined_data.csv
    """

    # make directory /data
    Path("processed_data/uber").mkdir(exist_ok = True) 
    all_dataframes = []

    # get all the zipped files in the raw_data directory into the list all_dataframes
    files_to_unzip = [f for f in glob.glob(f"{data_paths_config.uber_raw_path}/*.zip") if "15" not in f]
   

    for file in files_to_unzip:
        with zipfile.ZipFile(file, 'r') as zip_ref:
           unzipped_file = zip_ref.namelist()[0]
           df = pd.read_csv(zip_ref.open(unzipped_file))
           all_dataframes.append(df)

    # concatenate into one big dataframe
    combined_df = pd.concat(all_dataframes)
    combined_df['Date/Time'] = pd.to_datetime(combined_df['Date/Time'])
    combined_df.to_csv(data_paths_config.uber_processed_csv, index=False)
    

    # calculate % of duplicates and drop them
    percentage_of_dupes = combined_df.duplicated().sum() /len(combined_df) * 100
    print("Percentage of combined data are duplicates: {:.2f}%".format(percentage_of_dupes))

    combined_df = combined_df.drop_duplicates()
    print("Cleaned duplicates in Uber data.")

    return combined_df