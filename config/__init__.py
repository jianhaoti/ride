from pathlib import Path
import pandas as pd
import yaml
from typing import List

def load_config(config_names: List[str]):
    configs = {}

    for config_name in config_names:
        config_path = Path(__file__).parent / f"{config_name}_config.yaml"
        with open(config_path, 'r') as file:
            configs[config_name] = yaml.safe_load(file)

    return configs

configs = load_config(["analysis", "data_paths"])

class DataPathsConfig:
    def __init__(self, config):
        # Uber
        self.uber_raw_path = config['uber_raw_path']
        self.uber_processed_path = config['uber_processed_path']
        self.uber_processed_csv = config['uber_processed_csv']

        # Weather
        self.weather_raw_psv = config['weather_raw_psv']
        self.weather_raw_path = config['weather_raw_path']
        self.weather_processed_path = config['weather_processed_path']


class AnalysisConfig:
    def __init__(self, analysis_cfg, data_paths_cfg):
        # temporal 
        self.days_of_week = analysis_cfg['temporal']['days_of_week']
        self.colors = pd.Series(analysis_cfg['temporal']['colors'])

        # clustering
        self.sample_sizes = analysis_cfg['clustering']['sample_sizes']
        self.min_samples = analysis_cfg['clustering']['min_samples']
        self.eps = analysis_cfg['clustering']['eps']

        # paths
        self.input_path = data_paths_cfg.uber_processed_path
        self.output_path_dbscan = analysis_cfg['output_path_dbscan']
        self.output_path_temporal = analysis_cfg['output_path_temporal']

data_paths_config = DataPathsConfig(configs['data_paths'])
analysis_config = AnalysisConfig(configs['analysis'], data_paths_config)