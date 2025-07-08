from rich.console import Console
from rich.table import Table
from typing import Dict
import pandas as pd

import matplotlib.pyplot as plt

from config import analysis_config

from analysis.temporal_analysis import run_temporal_analysis

def plot_scatterplot(coords):
    """Plot scatter plot of coordinates (handles both DataFrame and numpy array)"""
    if isinstance(coords, pd.DataFrame):
        # DataFrame with 'Longitude' and 'Latitude' columns
        plt.scatter(x=coords['Longitude'], y=coords['Latitude'], alpha=0.5, s=1)
    else:
        # Numpy array with [lat, lon] or [lon, lat] format
        plt.scatter(x=coords[:, 1], y=coords[:, 0], alpha=0.5, s=1)
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Uber Pickup Locations')
    plt.show()


def display_cluster_results_to_console(cluster: Dict[int, pd.DataFrame]):
    console = Console()
    table = Table(title=f"DBSCAN Cluster Results for ε = {analysis_config.eps}")

    # Add columns
    table.add_column("Sample Size", style="cyan")
    for min_sample in analysis_config.min_samples:
        table.add_column(f"ms = {min_sample}", style="green")

    # Add rows
    for i, sample_size in  enumerate(analysis_config.sample_sizes):
        clustering_results = cluster[sample_size]

        # number of clusters
        row = [f"{sample_size:,}"]
        for min_sample in analysis_config.min_samples:
            number_of_clusters = clustering_results.loc[min_sample, 'num_clusters']
            row.append(str(number_of_clusters))
        table.add_row(*row)

        # percent that the largest cluster takes.
        percent_row = ["largest cluster %"]
        for min_sample in analysis_config.min_samples:
            percent = clustering_results.loc[min_sample, 'percent']
            percent_row.append(str(percent))
        table.add_row(*percent_row)

        # Add an empty row for spacing, except last one
        if i < len(analysis_config.sample_sizes) - 1:
            table.add_row(*[""] * (len(analysis_config.min_samples) + 1))
    
    console.print(table)
    


def plot_line_graph(density_dict, title="Weekend versus Weekday by Hour", xlabel='Hour of Day', ylabel='Avg Rides per Hour per Day', save_path=None):
    plt.figure(figsize=(12, 7))
    for label, (density, color) in density_dict.items():
        plt.plot(density.index, density.values, label=label, marker='o', color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.xticks(range(24))
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_bar_graph(day_density_dict, title="Avg Rides per Day by Day of Week", save_path=None):
    # Extract day names, densities, and colors from the dictionary
    day_names = list(day_density_dict.keys())
    densities = [v[0] for v in day_density_dict.values()]
    colors = [v[1] for v in day_density_dict.values()]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(day_names, densities, color=colors)
    plt.xlabel('Day of Week')
    plt.ylabel('Avg Rides per Day')
    plt.title(title)
    plt.grid(axis='y')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def display_temporal_analysis():
    from config import analysis_config
    
    temporal_results = run_temporal_analysis()
    
    # Plot weekday vs weekend patterns
    plot_line_graph(
        temporal_results['weekday_weekend'], 
        title="Weekday vs Weekend Patterns",
        save_path=f"{analysis_config.output_path}/weekday_weekend_patterns.png"
    )

    # Plot daily patterns
    plot_bar_graph(
        temporal_results['every_day'], 
        title="Daily Ride Patterns",
        save_path=f"{analysis_config.output_path}/daily_patterns.png"
    )

    # Plot hourly patterns by day
    plot_line_graph(
        temporal_results['per_hour'], 
        title="Hourly Patterns by Day",
        save_path=f"{analysis_config.output_path}/hourly_patterns_by_day.png"
    )


def plot_interactive_map(df):
    """Simple interactive map using plotly.express with lon/lat DataFrame"""
    import plotly.express as px
    import plotly.io as pio
    
    # Configure to open in browser
    pio.renderers.default = "chrome"

    fig = px.scatter_mapbox(
        df,
        lat='Lat',
        lon='Lon',
        zoom=10,
        mapbox_style='open-street-map',
        title='Uber Pickup Locations',
        opacity=0.6
    )
    
    fig.update_layout(
        title_x=0.5,
        margin={"r":0,"t":50,"l":0,"b":0},
        height=600
    )
    fig.show()

def plot_heatmap(df):
    """Create a heatmap showing Uber pickup hotspots using Plotly"""
    import plotly.express as px
    import plotly.io as pio
    
    # Configure to open in browser
    pio.renderers.default = "chrome"
    
    # Create heatmap using density
    fig = px.density_mapbox(
        df,
        lat='Lat',
        lon='Lon',
        zoom=10,
        mapbox_style='open-street-map',
        title='Uber Pickup Hotspots',
        radius=20,  # Size of each point's influence
        opacity=0.7
    )
    
    fig.update_layout(
        title_x=0.5,
        margin={"r":0,"t":50,"l":0,"b":0},
        height=600
    )
    
    fig.show()

def plot_hexbin_map(df):
    """Create a hexbin map showing pickup density using Plotly"""
    import plotly.express as px
    import plotly.io as pio
    
    # Configure to open in browser
    pio.renderers.default = "chrome"
    
    # Create hexbin map
    fig = px.scatter_mapbox(
        df,
        lat='Lat',
        lon='Lon',
        zoom=10,
        mapbox_style='open-street-map',
        title='Uber Pickup Density (Hexbin)',
        opacity=0.6,
        size_max=15
    )
    
    # Add hexbin layer
    fig.add_trace(
        px.scatter_mapbox(
            df,
            lat='Lat',
            lon='Lon',
            color_discrete_sequence=['red'],
            opacity=0.3
        ).data[0]
    )
    
    fig.update_layout(
        title_x=0.5,
        margin={"r":0,"t":50,"l":0,"b":0},
        height=600
    )
    
    fig.show()

