import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import pandas as pd

# Import your generated samples and continuous specs
from elhs import all_samples, cont_specs

# Threshold ratio for flagging (min_dist < threshold_ratio * avg_nn)
threshold_ratio = 0.5

diagnostics = []

for pcell, samples in all_samples.items():
    specs = cont_specs[pcell]
    
    # Build flat list of continuous dims spec: (name, min, max) per dimension
    flat_specs = []
    for name, mn, mx, cnt in specs:
        flat_specs.extend([(name, mn, mx)] * cnt)
    
    n_p = len(samples)
    d_p = len(flat_specs)
    
    # Reconstruct normalized continuous matrix
    cont_matrix = np.zeros((n_p, d_p))
    for i, sample in enumerate(samples):
        for j, (name, mn, mx) in enumerate(flat_specs):
            val = sample[name][j]
            cont_matrix[i, j] = (val - mn) / (mx - mn)
    
    # Compute pairwise distances
    dist_matrix = squareform(pdist(cont_matrix))
    np.fill_diagonal(dist_matrix, np.inf)
    min_dist = np.min(dist_matrix)
    nn_dist = np.min(dist_matrix, axis=1)
    avg_nn = np.mean(nn_dist)
    flagged = min_dist < threshold_ratio * avg_nn
    
    diagnostics.append({
        'pcell': pcell,
        'min_distance': min_dist,
        'avg_nearest_neighbor': avg_nn,
        'flagged': flagged
    })
    
    # Plot histograms for each continuous dimension
    for j, (name, mn, mx) in enumerate(flat_specs):
        values = [sample[name][j] for sample in samples]
        plt.figure()
        plt.hist(values, bins=20)
        plt.title(f"{pcell} — {name}[{j}] histogram")
        plt.xlabel(name)
        plt.ylabel("Frequency")
        plt.show()

# Display diagnostics table
df_diag = pd.DataFrame(diagnostics)
df_diag
