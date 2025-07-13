import pandas as pd
import pytest
import feature_engineering as fe  # your module with add_is_event_feature

def test_matching_event_sets_is_event_true():
    ride_df = pd.DataFrame([
        {'Date/Time': '2014-07-01 00:03:00', 'Lat': 40.7586, 'Lon': -73.9706, 'H3 Index': '892a100d607ffff'}
    ])
    
    event_df = pd.DataFrame([{
        'Start Military Time': '2014-07-01 00:00:00',
        'Close Military Time': '2014-07-01 00:10:00',
        'Event H3 Index': '892a100d607ffff',
        'Facility': 'Test',
        'Organization': 'Org'
    }])

    ride_df['Date/Time'] = pd.to_datetime(ride_df['Date/Time'])
    event_df['Start Military Time'] = pd.to_datetime(event_df['Start Military Time'])
    event_df['Close Military Time'] = pd.to_datetime(event_df['Close Military Time'])

    result = fe.add_is_event_feature(ride_df, event_df)
    assert result['Is Event'].iloc[0] == True
    #access first row

def test_no_overlapping_events_returns_all_false():
    ride_df = pd.DataFrame([
        {'Date/Time': '2014-07-02 00:03:00', 'Lat': 40.7586, 'Lon': -73.9706, 'H3 Index': '892a100d607ffff'}
    ])
    
    event_df = pd.DataFrame([{
        'Start Military Time': '2014-07-01 00:00:00',
        'Close Military Time': '2014-07-01 00:10:00',
        'Event H3 Index': '892a100d607ffff',
        'Facility': 'Test',
        'Organization': 'Org'
    }])

    ride_df['Date/Time'] = pd.to_datetime(ride_df['Date/Time'])
    event_df['Start Military Time'] = pd.to_datetime(event_df['Start Military Time'])
    event_df['Close Military Time'] = pd.to_datetime(event_df['Close Military Time'])

    result = fe.add_is_event_feature(ride_df, event_df)
    assert result['Is Event'].iloc[0] == False

def test_events_with_missing_values_are_skipped():
    ride_df = pd.DataFrame([
        {'Date/Time': '2014-07-01 00:05:00', 'Lat': 40.7586, 'Lon': -73.9706, 'H3 Index': '892a100d607ffff'}
    ])
    
    event_df = pd.DataFrame([
        {'Start Military Time': pd.NaT, 'Close Military Time': '2014-07-01 00:10:00', 'Event H3 Index': '892a100d607ffff', 'Facility': '', 'Organization': ''},
        {'Start Military Time': '2014-07-01 00:00:00', 'Close Military Time': pd.NaT, 'Event H3 Index': '892a100d607ffff', 'Facility': '', 'Organization': ''},
        {'Start Military Time': '2014-07-01 00:00:00', 'Close Military Time': '2014-07-01 00:10:00', 'Event H3 Index': pd.NA, 'Facility': '', 'Organization': ''}
    ])

    event_df['Start Military Time'] = pd.to_datetime(event_df['Start Military Time'], errors='coerce')
    event_df['Close Military Time'] = pd.to_datetime(event_df['Close Military Time'], errors='coerce')
    ride_df['Date/Time'] = pd.to_datetime(ride_df['Date/Time'])

    result = fe.add_is_event_feature(ride_df, event_df)
    assert result['Is Event'].iloc[0] == False
