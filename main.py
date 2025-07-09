import pandas as pd
from pathlib import Path
from rich.console import Console

from data.processing.process_uber_data import process_2014_data
from feature_engineering import add_temporal_features

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
    combined_data_df = process_2014_data() if not csv_path.exists() else pd.read_csv(csv_path, parse_dates=['Date/Time'])
    combined_data_df = add_features(combined_data_df)
    print(combined_data_df.head())

    # Spatial 
    coords = data_pipeline.get_spatial_data()

    # Plotly Visualization
    # plot_interactive_map(coords)
    # plot_heatmap(coords)
    # plot_hexbin_map(coords)

    # DBSCAN
    print("\nResults using DBSCAN")
    print("------------------------------------------------------------------")

    run_spatial_analysis(coords)

    # Temporal 
    # temporal = data_pipeline.get_temporal_data()
    # earliest_date = temporal['Date/Time'].min()
    # latest_date = temporal['Date/Time'].max()
    # console.log(f"Earliest date is {earliest_date} and latest date is {latest_date}.")

    # display_temporal_analysis()


