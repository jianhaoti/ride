import pandas as pd
import h3
from feature_engineer_events import process_511_ny_events, add_h3_index_event

def find_event_by_h3(target_h3="892a100d5dbffff"):
    """
    Find the event that corresponds to a specific H3 index
    """
    print(f"Looking for event with H3 index: {target_h3}")
    
    # Load and process the events data
    df = pd.read_csv("raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv")
    print(f"Loaded {len(df)} events from CSV")
    
    # Process the events data
    df = process_511_ny_events(df)
    df = add_h3_index_event(df, "Latitude", "Longitude")
    
    # Find the event with the target H3 index
    matching_events = df[df['Event H3 Index'] == target_h3]
    
    if len(matching_events) == 0:
        print(f"No events found with H3 index: {target_h3}")
        return None
    
    print(f"\nFound {len(matching_events)} event(s) with H3 index {target_h3}:")
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
    
    return matching_events

if __name__ == "__main__":
    # Find the specific event
    events = find_event_by_h3("892a100d5dbffff")
    
    if events is not None:
        print("\nAll columns in the matching event(s):")
        print(events.columns.tolist()) 