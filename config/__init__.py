from pathlib import Path
import pandas as pd
import yaml

def load_config(config_name: str ):
    config_path = Path(__file__).parent / f"{config_name}_config.yaml"
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

raw_analysis_config = load_config("analysis")

class AnalysisConfig:
    def __init__(self, config):
        # temporal 
        self.days_of_week = config['temporal']['days_of_week']
        self.colors = pd.Series(config['temporal']['colors'])

        # clustering
        self.sample_sizes = config['clustering']['sample_sizes']
        self.min_samples = config['clustering']['min_samples']
        self.eps = config['clustering']['eps']

        # paths
        self.input_path = config['data']['input_path']
        self.output_path = config['data']['output_path']

analysis_config = AnalysisConfig(raw_analysis_config)
