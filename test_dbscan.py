import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Create synthetic data with clear clusters
np.random.seed(42)
n_samples = 1000

# Create 3 clear clusters
cluster1 = np.random.normal([0, 0], 0.5, (n_samples//3, 2))
cluster2 = np.random.normal([5, 5], 0.5, (n_samples//3, 2))
cluster3 = np.random.normal([10, 0], 0.5, (n_samples//3, 2))

# Add some noise
noise = np.random.uniform(-2, 12, (n_samples//10, 2))

# Combine all data
data = np.vstack([cluster1, cluster2, cluster3, noise])

# Standardize
scaler = StandardScaler()
data_std = scaler.fit_transform(data)

print("Testing DBSCAN monotonicity with synthetic data:")
print(f"Data shape: {data_std.shape}")
print(f"Data range: {data_std.min():.2f} to {data_std.max():.2f}")

# Test different min_samples values
min_samples_values = [5, 10, 15, 20, 25]
eps = 0.5

print(f"\neps = {eps}")
print("min_samples | clusters | noise_points")
print("-" * 35)

for min_samples in min_samples_values:
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(data_std)
    labels = clustering.labels_
    unique_labels = set(labels)
    num_clusters = len([label for label in unique_labels if label != -1])
    num_noise = np.sum(labels == -1)
    
    print(f"{min_samples:10d} | {num_clusters:8d} | {num_noise:12d}") 