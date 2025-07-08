import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from config import analysis_config
# Load your data
df = pd.read_csv("processed_data/combined_data_with_features.csv", parse_dates=['Date/Time'])
coords = df[['Lat', 'Lon']].to_numpy()

# Apply standardization (same as in your pipeline)
scaler = StandardScaler()
coords_std = scaler.fit_transform(coords)

# Get scaling factors
lat_scale = scaler.scale_[0] #type:ignore
lon_scale = scaler.scale_[1] #type:ignore

print(f"Original coordinate ranges:")
print(f"Latitude:  {coords[:, 0].min():.6f} to {coords[:, 0].max():.6f}")
print(f"Longitude: {coords[:, 1].min():.6f} to {coords[:, 1].max():.6f}")

print(f"\nScaling factors:")
print(f"Latitude scale:  {lat_scale:.6f}")
print(f"Longitude scale: {lon_scale:.6f}")

# Convert eps=0.001 back to original degrees
eps_lat_deg = analysis_config.eps * lat_scale
eps_lon_deg = analysis_config.eps * lon_scale

print(f"\neps={analysis_config.eps} in standardized units converts to:")
print(f"Latitude:  {eps_lat_deg:.6f} degrees")
print(f"Longitude: {eps_lon_deg:.6f} degrees")

# Convert to feet
avg_lat = coords[:, 0].mean()
cos_lat = np.cos(np.radians(avg_lat))

# 1 degree ≈ 69 miles ≈ 364,320 feet
lat_feet = eps_lat_deg * 364320
lon_feet = eps_lon_deg * 364320 * cos_lat

print(f"\nApproximate distance in feet:")
print(f"Latitude direction:  {lat_feet:.1f} feet")
print(f"Longitude direction: {lon_feet:.1f} feet")
print(f"Average:            {(lat_feet + lon_feet) / 2:.1f} feet")

print(f"\nAverage latitude: {avg_lat:.2f}°N")
print(f"cos(latitude) = {cos_lat:.3f}") 