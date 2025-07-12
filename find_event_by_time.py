import pandas as pd
from datetime import datetime
from feature_engineer_events import process_511_ny_events, add_h3_index_event

def find_event_by_time(target_time="2014-07-01 12:56:00", 
                      start_time="2010-04-09 03:23:58", 
                      close_time="2010-04-10 11:26:55"):
    """
    Find events that match the specific time parameters
    """
    print(f"Looking for events with:")
    print(f"  Target time: {target_time}")
    print(f"  Start time: {start_time}")
    print(f"  Close time: {close_time}")
    print("=" * 80)
    
    # Load and process the events data
    df = pd.read_csv("raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv")
    print(f"Loaded {len(df)} events from CSV")
    
    # Process the events data
    df = process_511_ny_events(df)
    df = add_h3_index_event(df, "Latitude", "Longitude")
    
    # Convert times to datetime for comparison
    target_dt = pd.to_datetime(target_time)
    start_dt = pd.to_datetime(start_time)
    close_dt = pd.to_datetime(close_time)
    
    print(f"\nConverted times:")
    print(f"  Target: {target_dt}")
    print(f"  Start:  {start_dt}")
    print(f"  Close:  {close_dt}")
    
    # Find events that match the time window
    matching_events = df[
        (df['Start Military Time'] == start_time) & 
        (df['Close Military Time'] == close_time)
    ]
    
    print(f"\nFound {len(matching_events)} event(s) with matching start/close times:")
    print("=" * 80)
    
    for idx, event in matching_events.iterrows():
        print(f"Event Name: {event.get('Event Name', 'N/A')}")
        print(f"Event Type: {event.get('Event Type', 'N/A')}")
        print(f"Venue: {event.get('Venue', 'N/A')}")
        print(f"Latitude: {event.get('Latitude', 'N/A')}")
        print(f"Longitude: {event.get('Longitude', 'N/A')}")
        print(f"Start Time: {event.get('Start Military Time', 'N/A')}")
        print(f"Close Time: {event.get('Close Military Time', 'N/A')}")
        print(f"H3 Index: {event.get('Event H3 Index', 'N/A')}")
        print("-" * 80)
    
    # Also check if the target time falls within any event's time window
    print(f"\nChecking if target time {target_time} falls within any event's time window...")
    time_matching_events = df[
        (df['Start Military Time'] <= target_time) & 
        (df['Close Military Time'] >= target_time)
    ]
    
    print(f"Found {len(time_matching_events)} event(s) where target time falls within event window:")
    print("=" * 80)
    
    for idx, event in time_matching_events.iterrows():
        print(f"Event Name: {event.get('Event Name', 'N/A')}")
        print(f"Event Type: {event.get('Event Type', 'N/A')}")
        print(f"Venue: {event.get('Facility Name', 'N/A')}")
        print(f"Latitude: {event.get('Latitude', 'N/A')}")
        print(f"Longitude: {event.get('Longitude', 'N/A')}")
        print(f"Start Time: {event.get('Start Military Time', 'N/A')}")
        print(f"Close Time: {event.get('Close Military Time', 'N/A')}")
        print(f"H3 Index: {event.get('Event H3 Index', 'N/A')}")
        print("-" * 80)
    
    return matching_events, time_matching_events

if __name__ == "__main__":
    # Find events matching the specific time parameters
    exact_matches, time_matches = find_event_by_time(
        target_time="2014-07-01 12:56:00",
        start_time="2010-04-09 03:23:58", 
        close_time="2010-04-10 11:26:55"
    ) 