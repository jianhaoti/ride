import pandas as pd
from datetime import datetime
import h3 
def add_start_military_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert time column to military (24-hour) format
    """

    df['Create Time'] = pd.to_datetime(df['Create Time'], format="%m/%d/%Y %I:%M:%S %p")
    df['Start Military Time'] = df['Create Time'].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def add_close_military_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert time column to military (24-hour) format
    """

    df['Close Time'] = pd.to_datetime(df['Close Time'], format="%m/%d/%Y %I:%M:%S %p")
    df['Close Military Time'] = df['Close Time'].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def add_event_duration(df: pd.DataFrame, start_time_col: str, end_time_col: str) -> pd.DataFrame:
    """
    Calculate event duration in hours
    """
    # Add duration calculation logic here
    return df

def add_event_type_category(df: pd.DataFrame, event_type_col: str) -> pd.DataFrame:
    """
    Categorize events into broader types (sports, concert, etc.)
    """
    # Add categorization logic here
    return df

def add_is_major_event(df: pd.DataFrame, event_type_col: str) -> pd.DataFrame:
    """
    Create boolean flag for major events that might significantly impact ride demand
    """
    # Add logic to identify major events
    return df

def add_event_day_of_week(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Extract day of week from event date
    """
    # Add day of week extraction logic
    return df

def add_event_hour_of_day(df: pd.DataFrame, time_column: str) -> pd.DataFrame:
    """
    Extract hour of day from event time
    """
    # Add hour extraction logic
    return df

def is_valid_lat_lng(lat, lng):
    """
    Check if latitude and longitude are valid coordinates
    """
    return -90 <= lat <= 90 and -180 <= lng <= 180 and (lat != 0.0 or lng != 0.0)

def add_h3_index_event(df: pd.DataFrame, latitude_column: str, longitude_column: str) -> pd.DataFrame:
    """
    Add H3 index for event location
    """
    # Filter out invalid coordinates to prevent H3 errors
    initial_count = len(df)
    df = df[df.apply(lambda row: is_valid_lat_lng(row[latitude_column], row[longitude_column]), axis=1)].copy()
    filtered_count = len(df)
    print(f"Filtered out {initial_count - filtered_count} events with invalid coordinates (kept {filtered_count} events)")
    
    df['Event H3 Index'] = df.apply(lambda row: h3.latlng_to_cell(row[latitude_column], row[longitude_column], 9), axis=1)
    return df 


# Example usage functions (you'll need to implement the actual logic)
def process_511_ny_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all event feature engineering functions
    """
    # Add your processing pipeline here
    # df = add_military_time(df, 'your_time_column')
    # df = add_event_duration(df, 'start_time', 'end_time')
    # etc.
    
    df = add_start_military_time(df)
    df = add_close_military_time(df)
    return df


if __name__ == "__main__":
    print(h3.__version__)
    df = pd.read_csv("raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv")
    df = process_511_ny_events(df)
    df = add_h3_index_event(df, "Latitude", "Longitude")
    print(df.head())
    