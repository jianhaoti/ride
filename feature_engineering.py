import pandas as pd
from pathlib import Path
import h3
import feature_engineer_events as fe
from data.processing.process_uber_data import process_2014_data
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
    df['H3 Index'] = df.apply(lambda row: h3.latlng_to_cell(row["Lat"], row["Lon"], 9), axis=1)
    return df
    
# def add_is_event_feature(ride_df: pd.DataFrame, event_df: pd.DataFrame) -> pd.DataFrame:
#     """
#     For each ride, check if it occurs within 3 H3 steps and time window of any event
#     """
#     # Ensure time columns are datetime
#     ride_df['Date/Time'] = pd.to_datetime(ride_df['Date/Time'])
#     event_df['Start Military Time'] = pd.to_datetime(event_df['Start Military Time'])
#     event_df['Close Military Time'] = pd.to_datetime(event_df['Close Military Time'])

#     # Apply row-wise
#     ride_df['Is Event'] = ride_df.apply(
#         lambda row: any(
#             h3.grid_distance(row['H3 Index'], event_h3) <= 3 and
#             start_time <= row['Date/Time'] <= close_time
#             for event_h3, start_time, close_time in zip(
#                 event_df['Event H3 Index'],
#                 event_df['Start Military Time'],
#                 event_df['Close Military Time']
#             )
#         ),
#         axis=1
#     )

#     return ride_df




def is_near_event(event_facility, event_org, ride_h3, ride_time, event_h3, start_time, close_time):
    try:
        if not (start_time <= ride_time <= close_time):
            return False
            #short circuit 
        if pd.isna(ride_h3) or pd.isna(event_h3):
            return False
        if h3.get_resolution(ride_h3) != h3.get_resolution(event_h3):
            return False
        return (
            h3.grid_distance(ride_h3, event_h3) <= 3 and
            start_time <= ride_time <= close_time
        )
    except Exception as e:
        print(
            f"[H3 ERROR] ride_h3={ride_h3}, event_h3={event_h3}, "
            f"facility={event_facility}, organization={event_org}, "
            f"time={ride_time}, start={start_time}, close={close_time}, "
            f"error={type(e).__name__}: {e}"
        )
        return False


def add_is_event_feature(ride_df: pd.DataFrame, event_df: pd.DataFrame) -> pd.DataFrame:
    """
    For each ride, check if it occurs within 3 H3 steps and time window of any event
    Uses spatial and temporal indexing for much better performance
    """
    print(f"Processing {len(ride_df):,} rides against {len(event_df):,} events...")
    
    # Ensure time columns are datetime
    ride_df['Date/Time'] = pd.to_datetime(ride_df['Date/Time'])
    event_df['Start Military Time'] = pd.to_datetime(event_df['Start Military Time'])
    event_df['Close Military Time'] = pd.to_datetime(event_df['Close Military Time'])
    
    # Create a copy to avoid modifying original
    ride_df = ride_df.copy()
    
    # Initialize the Is Event column
    ride_df['Is Event'] = False
    
    # Get the time range of rides to filter events
    ride_start = ride_df['Date/Time'].min()
    ride_end = ride_df['Date/Time'].max()
    print(f"Ride time range: {ride_start} to {ride_end}")
    
    # Filter events to only those that overlap with ride time range
    time_filtered_events = event_df[
        (event_df['Close Military Time'] >= ride_start) & 
        (event_df['Start Military Time'] <= ride_end)
    ].copy()
    
    print(f"Filtered to {len(time_filtered_events)} events that overlap with ride time range")
    
    if len(time_filtered_events) == 0:
        print("No events overlap with ride time range")
        return ride_df
    
    # Process events in batches
    batch_size = 50  # Smaller batch size for better memory management
    total_events = len(time_filtered_events)
    
    for i in range(0, total_events, batch_size):
        end_idx = min(i + batch_size, total_events)
        event_batch = time_filtered_events.iloc[i:end_idx]
        
        print(f"Processing events {i+1}-{end_idx} of {total_events}...")
        
        # For each event in the batch, find matching rides
        for _, event in event_batch.iterrows():
            event_h3 = event['Event H3 Index']
            start_time = event['Start Military Time']
            close_time = event['Close Military Time']
            
            # Skip invalid events
            if pd.isna(event_h3) or pd.isna(start_time) or pd.isna(close_time):
                continue
            
            # Find rides that are within the time window
            time_mask = (ride_df['Date/Time'] >= start_time) & (ride_df['Date/Time'] <= close_time)
            
            if not time_mask.any():
                continue
            
            # For rides in the time window, check spatial proximity
            time_filtered_rides = ride_df[time_mask]
            
            # Check H3 grid distance for rides in time window
            spatial_mask = time_filtered_rides['H3 Index'].apply(
                lambda ride_h3: h3.grid_distance(ride_h3, event_h3) <= 3 if pd.notna(ride_h3) else False
            )
            
            # Mark matching rides as events
            matching_indices = time_filtered_rides[spatial_mask].index
            ride_df.loc[matching_indices, 'Is Event'] = True
    
    event_count = ride_df['Is Event'].sum()
    print(f"Found {event_count:,} rides near events ({event_count/len(ride_df)*100:.2f}%)")
    
    return ride_df





#     ride_df = pd.read_csv("rocessed_data/combined_data.csv"")
#     event_df = pd.read_csv("raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv")
#     ride_df = add_h3_9(ride_df)
#     event_df = fe.add_h3_index_event(event_df, "latitude", "longitude")
#     ride_df = add_is_event_feature(ride_df, event_df)
#     print(ride_df.head())


#logic in rows...
#checks every row in ride_df, for each row, it checks if the h3 index is within 3 steps of any event h3 index and if the date/time is within the start and close time of the event
#if it is, it adds a 1 to the is event column for that row
#both conditions must be satisfied 


#any is for loop with if condition, early exit as soon as mathc is found 



#any: for x in list: if condition(x), return True


    #my 12 hour clock format with AM/PM in my events data is 12 hour clock format with AM/PM...
    #the original kaggle data has 24 hour clock format with AM/PM..

    

if __name__ == "__main__":
    print(h3.cell_to_latlng("89754e64993ffff"))