import pandas as pd

def add_temporal_features(df:pd.DataFrame) -> pd.DataFrame:
    df['Is Weekend'] = df['Date/Time'].dt.dayofweek >= 5    
    df['Day Name'] = df['Date/Time'].dt.day_name()

    return df

def add_bool_rush_hour(df: pd.DataFrame) -> pd.DataFrame:
    df['Is Rush Hour'] = df['Date/Time'].dt.hour.isin([6,7, 8, 16, 17, 18])  & (~ df['Is Weekend']) 
    return df


    