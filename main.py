import pandas as pd
from pathlib import Path
from rich.console import Console

from data.pipeline import DataPipeline
from processing.process_uber_data import process_uber_data
from feature_engineering import add_temporal_features
from event_df.feature_engineer_events import add_h3_index_event
from feature_engineering import add_h3_9

from analysis.visualization import display_temporal_analysis, plot_hexbin_map, display_cluster_results_to_console
from analysis.spatial_analysis import find_number_of_clusters 
from data import data_pipeline
from config import analysis_config as anal, data_paths_config as dp

from processing.process_weather_data import filter_out_weather_column_metadata, obtain_weather_columns

from event_df.jasmines_main import jasmines_main
import unit_tests.test_feature_engineering as test_feature_engineering

console = Console()

def run_spatial_analysis(coords, save = True):
    Path(anal.output_path_dbscan).mkdir(parents=True, exist_ok=True)    

    cluster_dict =  find_number_of_clusters(coords)
    display_cluster_results_to_console(cluster_dict)
    
    if save: 
        for sample_size in anal.sample_sizes:
            df = cluster_dict[sample_size] 
            df.to_csv(f"{anal.output_path_dbscan}/clustering_result_sample_size_{sample_size}.csv")

    return cluster_dict    


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_temporal_features(df)
    df.to_csv(dp.uber_processed_csv, index=False)
    return df

if __name__ == "__main__":
    # csv_path = Path(f"{dp.uber_processed_csv}")

    # combined_data_df = process_uber_data() if not csv_path.exists() else pd.read_csv(csv_path, parse_dates=['Date/Time'])
    # combined_data_df = add_features(combined_data_df)

    # # # Spatial 
    # # coords = data_pipeline.get_spatial_data()

    # # # Plotly Visualization
    # # plot_hexbin_map(coords)

    # # # DBSCAN
    # # print("\nResults using DBSCAN")
    # # print("------------------------------------------------------------------")

    # # run_spatial_analysis(coords)

    # # Temporal 
    # temporal = data_pipeline.get_temporal_data()
    # # earliest_date = temporal['Date/Time'].min()
    # # latest_date = temporal['Date/Time'].max()
    # # console.log(f"Earliest date is {earliest_date} and latest date is {latest_date}.")

    # display_temporal_analysis()
    jasmines_main()
    # Run feature engineering tests using pytest
    import subprocess
    print("\nRunning feature engineering tests with pytest...")
    result = subprocess.run(['python3', '-m', 'pytest', 'unit_tests/test_feature_engineering.py', '-v'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Some tests failed!")
        print(result.stderr)
    else:
        print("✓ All tests passed!")




    # Weather
    # weather_csv = data_pipeline.get_weather_data()
    # obtain_weather_columns(weather_csv, output_path=)

    # print(weather_columns)
    # filter_out_weather_column_metadata()
