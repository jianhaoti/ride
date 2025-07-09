# ds libraires
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd

# import config and pipline
from config import analysis_config

# misc
from typing import Dict
from rich.progress import Progress

def find_number_of_clusters(coords) -> Dict[int, pd.DataFrame]:
    clustering_results = {} # key = sample_size, value indexed by min_sample with clustering info as entries
    #min_Sample means you need to have at least min_Sample points in a cluster to be considered a cluster
    
    with Progress() as progress:
        size_task = progress.add_task("Sample sizes", total=len(analysis_config.sample_sizes))
        min_task = progress.add_task("min_samples", total=len(analysis_config.min_samples))
        print(f"ε parameter set to {analysis_config.eps}")
        
        for sample_size in analysis_config.sample_sizes:
            progress.reset(min_task)
            
            coords_sample = coords.sample(n = sample_size)

            results_df = pd.DataFrame(index=analysis_config.min_samples, columns=['num_clusters', 'percent']) #type:ignore
            
            for min_sample in analysis_config.min_samples:
                clustering = DBSCAN(eps=analysis_config.eps, min_samples=min_sample).fit(coords_sample)
                labels = clustering.labels_
                unique_labels = set(labels)
                num_clusters = len(unique_labels) - (1 if -1 in labels else 0)
                results_df.loc[min_sample, 'num_clusters'] = num_clusters

                labels_no_noise = labels[labels != -1]
                counts = np.bincount(labels_no_noise)
                biggest_cluster_size = counts.max()

                percent = biggest_cluster_size / len(labels) * 100 if len(labels_no_noise) > 0 else 0.0
                results_df.loc[min_sample, 'percent'] = round(percent, 2)
                progress.advance(min_task)

            clustering_results[sample_size] = results_df
            progress.advance(size_task)
    return clustering_results

