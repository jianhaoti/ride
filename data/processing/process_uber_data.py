import pandas as pd
import zipfile
import glob
from pathlib import Path

def process_2014_data() -> pd.DataFrame:
    """
    1. take all the zipped files in the raw_data directory
    2. unzip files into the /data 
    3. combine files into a single dataframe
    4. return the dataframe into processed_data/combined_data.csv
    """
    # make directory /data
    Path("processed_data").mkdir(exist_ok = True) 
    all_dataframes = []

    # get all the zipped files in the raw_data directory into the list all_dataframes
    files_to_unzip = [f for f in glob.glob("raw_data/uber/*.zip") if "15" not in f]
    

    for file in files_to_unzip:
        with zipfile.ZipFile(file, 'r') as zip_ref:
           unzipped_file = zip_ref.namelist()[0]
           df = pd.read_csv(zip_ref.open(unzipped_file))
           all_dataframes.append(df)
        #    print(f"Number of duplicates in {unzipped_file}:", df.duplicated().sum())
           percentage_of_dupes = df.duplicated().sum() /len(df) * 100
           print("Percentage of data are duplicates: {:.2f}%".format(percentage_of_dupes))

    # concatenate into one big dataframe
    combined_df = pd.concat(all_dataframes)
    combined_df['Date/Time'] = pd.to_datetime(combined_df['Date/Time'])
    combined_df.to_csv("processed_data/combined_data.csv", index=False)
    
    # print("Combined raw data with reformatted Date/Time:", combined_df.head())
    # print("\nTypes:", combined_df.dtypes)


    # drop duplicates
    print("Total number of duplicates in combined dataset:", combined_df.duplicated().sum())
    percentage_of_dupes = combined_df.duplicated().sum() /len(combined_df) * 100
    print("Percentage of combined data are duplicates: {:.2f}%".format(percentage_of_dupes))

    combined_df = combined_df.drop_duplicates()
    print("Number of duplicates after cleaning:", combined_df.duplicated().sum())


    return combined_df