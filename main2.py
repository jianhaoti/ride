import pandas as pd
from pathlib import Path
from rich.console import Console

from data.processing.process_uber_data import process_2014_data
from feature_engineering import add_is_event_feature
from feature_engineer_events import process_511_ny_events
from feature_engineering import add_temporal_features
from feature_engineer_events import add_h3_index_event
from feature_engineering import add_h3_9

from analysis.visualization import display_temporal_analysis, plot_hexbin_map, display_cluster_results_to_console
from analysis.spatial_analysis import find_number_of_clusters 
from data import data_pipeline
from config import analysis_config
from analysis.visualization import plot_hexbin_map, plot_heatmap


console = Console()

def run_spatial_analysis(coords, save = True):
    cluster_dict =  find_number_of_clusters(coords)
    display_cluster_results_to_console(cluster_dict)

    if save: 
        for sample_size in analysis_config.sample_sizes:
            df = cluster_dict[sample_size] 
            df.to_csv(f"results/dbscan/clustering_result_sample_size_{sample_size}.csv")

    return cluster_dict    


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_temporal_features(df)
    df.to_csv("processed_data/combined_data_with_features.csv", index=False)
    return df

if __name__ == "__main__":
    csv_path = Path("processed_data/combined_data.csv")
    #what does this do?

    combined_data_df = process_2014_data() if not csv_path.exists() else pd.read_csv(csv_path, parse_dates=['Date/Time'])
    #if csv_path ecists, read it, if not, process the data
    combined_data_df = add_features(combined_data_df)
    combined_data_df = add_h3_9(combined_data_df)
    print(combined_data_df.head())

    # Skip DBSCAN for now - it's causing the freeze
    print("\nSkipping DBSCAN clustering to test event features...")

    # Event Data - Test with very small subset
    print("\nLoading event data...")
    event_df = pd.read_csv("raw_data/uber/511_NY_Sporting__Concert__and_Special_Events__Beginning_2010_20250709.csv")
    print(f"Loaded {len(event_df)} events")
    
    event_df = process_511_ny_events(event_df)
    event_df = add_h3_index_event(event_df, "Latitude", "Longitude")
    
    # Test with a very small subset first
    print("\nTesting event feature with very small subset...")
    test_rides = combined_data_df.head(1000)  # Test with first 100 rides only
    print(f"Testing with {len(test_rides)} rides and {len(event_df)} events")
    
    test_result = add_is_event_feature(test_rides, event_df)
    print(f"Test completed successfully!")
    print("Sample results:")
    print(test_result[['Date/Time', 'Lat', 'Lon', 'Is Event']].head(10000))
    
    # Save the test results
    print(test_result.columns, "this is columns")
    test_result.to_csv("processed_data/test_event_results2.csv", index=False)
    print("Test results saved to processed_data/test_event_results.csv")
    
    # Don't run the full dataset yet - let's verify the test works first
    print("\nTest completed. Full dataset processing skipped for now.")




#before coding, actually try functions in main....
#to make sure the function name is imported correctly...
#experiment,...



#if my main.py code processes many entries, can i create a version that restricts to a subset of the entries (say top 5) for testing purposes?
