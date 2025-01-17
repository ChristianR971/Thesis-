import numpy as np
from scipy.optimize import linprog

# Outputs (columns: Emission_reductions, Employment, VA)
Y = np.array([
    [0.3532, 1, 1],
    [0.1387, 0.4219, 0.3832],
    [1, 0.053, 0.0012],
    [0.7307, 0.0614, 0.0125],
    [0.0656, 0.4967, 0.4493],
    [0.6727, 0.1, 0.051],
    [0.0481, 0.5156, 0.466],
    [0.0464, 0.517, 0.4672],
    [0.0494, 0.5168, 0.4669],
    [0.0652, 0.5051, 0.457],
    [0.1295, 0.4964, 0.444],
    [0.0000001, 0.5798, 0.532],
    [0.8321, 0.6954, 0.6861],
    [0.1601, 0.6702, 0.6184],
    [0.825, 0.3363, 0.2657],
])

n_dmus, n_outputs = Y.shape
efficiency_scores = []

# DEA for each DMU
for i in range(n_dmus):
    # Target DMU's outputs
    y_o = Y[i]
    
    # Objective function (maximize weighted outputs for DMU i)
    c = -y_o  # Negative because linprog minimizes
    
    # Constraints (outputs of all DMUs ≤ 1 under the same weights)
    A = Y
    b = np.ones(n_dmus)
    
    # Bounds for weights (non-negativity)
    bounds = [(0, None)] * n_outputs
    
    # Solve the LP
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    
    # Efficiency score for DMU i
    efficiency = -result.fun if result.success else 0
    efficiency_scores.append(efficiency)

# Print results
for i, score in enumerate(efficiency_scores):
    print(f"Efficiency of DMU{i+1}: {score:.4f}")
