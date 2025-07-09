import pandas as pd

def add_temporal_features(df:pd.DataFrame) -> pd.DataFrame:
    df['Is Weekend'] = df['Date/Time'].dt.dayofweek >= 5    
    df['Day Name'] = df['Date/Time'].dt.day_name()

    return df

def add_bool_rush_hour(df: pd.DataFrame) -> pd.DataFrame:
    df['Is Rush Hour'] = df['Date/Time'].dt.hour.isin([6,7, 8, 16, 17, 18])  & (~ df['Is Weekend']) 
    return df

def add_hour_of_day(df: pd.DataFrame) -> pd.DataFrame:
    df['Hour of Day'] = df['Date/Time'].dt.hour
    return df 

def add_h3_9(df:pd.DataFrame) -> pd.DataFrame:
    df['H3 Index'] = df.apply(lambda row: h3.geo_to_h3(row["latitude"], row["longitude"], 9), axis=1)
    