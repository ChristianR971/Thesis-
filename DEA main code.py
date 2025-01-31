# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:50:33 2025

@author: C-att
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table

# Data
data = {
    "Delta_E": [-133445246.7, -55670368.69, -443765389.2, -322227406.4, -11929365.34,
                -294962016.6, -1211036.994, -126079.5192, -611000.7581, -9800299.349,
                -37856338.05, 22871104.13, -318539489.7, -35632533.43, -334958556.1],
    "Delta_Emp": [9.114687303, -1.795646081, -8.75869875, -8.59932818, -0.384781324, 
                   -7.871692884, -0.02785362, -0.001079969, -0.005233698, -0.225405011, 
                   -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282],
    "Delta_VA": [441.8022859, -69.66453618, -386.48829, -377.1394629, -14.92811568, 
                  -345.2276694, -1.047364889, -0.054375153, -0.263510378, -8.475785146, 
                  -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149]
}

# Proportional normalization with inverse for emissions
def proportional_normalize(column, inverse=False):
    shift = abs(min(column)) + 1
    shifted = [x + shift for x in column]
    normalized = [x / max(shifted) for x in shifted]
    return [1 - x for x in normalized] if inverse else normalized

normalized_data = {
    "Delta_E": proportional_normalize(data["Delta_E"], inverse=True),  # Inverse normalization for emissions
    "Delta_Emp": proportional_normalize(data["Delta_Emp"]),
    "Delta_VA": proportional_normalize(data["Delta_VA"])
}

# Plot table
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("tight")
ax.axis("off")

table_data = [[f"{x:.4f}" for x in normalized_data[key]] for key in normalized_data]
headers = list(normalized_data.keys())
rows = [f"DMU {i+1}" for i in range(len(next(iter(normalized_data.values()))))]

table = Table(ax, bbox=[0, 0, 1, 1])

# Add headers
for j, header in enumerate(headers):
    table.add_cell(0, j + 1, width=1 / (len(headers) + 1), height=0.3, text=header, loc='center', facecolor='lightgray')

# Add rows
table.add_cell(0, 0, width=0.15, height=0.3, text="DMU", loc='center', facecolor='lightgray')
for i, row in enumerate(rows):
    table.add_cell(i + 1, 0, width=0.15, height=0.3, text=row, loc='center', facecolor='white')
    for j, value in enumerate(table_data):
        table.add_cell(i + 1, j + 1, width=1 / (len(headers) + 1), height=0.3, text=value[i], loc='center', facecolor='white')

ax.add_table(table)
plt.show()
#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
import matplotlib.colors as mcolors

# Data
data = {
    "Delta_E": [-133445246.7, -55670368.69, -443765389.2, -322227406.4, -11929365.34,
                -294962016.6, -1211036.994, -126079.5192, -611000.7581, -9800299.349,
                -37856338.05, 22871104.13, -318539489.7, -35632533.43, -334958556.1],
    "Delta_Emp": [9.114687303, -1.795646081, -8.75869875, -8.59932818, -0.384781324, 
                   -7.871692884, -0.02785362, -0.001079969, -0.005233698, -0.225405011, 
                   -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282],
    "Delta_VA": [441.8022859, -69.66453618, -386.48829, -377.1394629, -14.92811568, 
                  -345.2276694, -1.047364889, -0.054375153, -0.263510378, -8.475785146, 
                  -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149]
}

# Proportional normalization with inverse for emissions
def proportional_normalize(column, inverse=False):
    shift = abs(min(column)) + 1
    shifted = [x + shift for x in column]
    normalized = [x / max(shifted) for x in shifted]
    return [1 - x for x in normalized] if inverse else normalized

normalized_data = {
    "Delta_E": proportional_normalize(data["Delta_E"], inverse=True),
    "Delta_Emp": proportional_normalize(data["Delta_Emp"]),
    "Delta_VA": proportional_normalize(data["Delta_VA"])
}

# Create color map function
def get_cell_color(value):
    # Create a custom colormap from intense red to white to intense blue
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#ff0000", "white", "#0000ff"])
    return cmap(value)

# Plot table
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("tight")
ax.axis("off")

table_data = [[f"{x:.4f}" for x in normalized_data[key]] for key in normalized_data]
headers = list(normalized_data.keys())
rows = [f"DMU {i+1}" for i in range(len(next(iter(normalized_data.values()))))]

# Create table
table = Table(ax, bbox=[0, 0, 1, 1])

# Add headers
for j, header in enumerate(headers):
    table.add_cell(0, j + 1, width=1 / (len(headers) + 1), height=0.3,
                  text=header, loc='center',
                  facecolor='lightgray')

# Add row headers
table.add_cell(0, 0, width=0.15, height=0.3,
              text="DMU", loc='center',
              facecolor='lightgray')

# Add data cells with colors
for i, row in enumerate(rows):
    table.add_cell(i + 1, 0, width=0.15, height=0.3,
                  text=row, loc='center',
                  facecolor='white')
    
    for j, values in enumerate(table_data):
        value = float(values[i])
        cell_color = get_cell_color(value)
        
        cell = table.add_cell(i + 1, j + 1,
                            width=1 / (len(headers) + 1),
                            height=0.3,
                            text=values[i],
                            loc='center',
                            facecolor=cell_color)
        
        # Adjust text color for better visibility
        if 0.3 <= value <= 0.7:
            cell.set_text_props(color='black')
        else:
            cell.set_text_props(color='white')

ax.add_table(table)

# Add a colorbar with intense colors
sm = plt.cm.ScalarMappable(cmap=mcolors.LinearSegmentedColormap.from_list("", ["#ff0000", "white", "#0000ff"]))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.046, pad=0.04)
cbar.set_label('Normalized Values')

plt.tight_layout()
plt.show()

#%%
import numpy as np
from scipy.optimize import linprog

# Outputs (columns: Emission_reductions, Employment, VA)
Y = np.array([
    [0.335, 1, 1],
    [0.1683, 0.4219, 0.3832],
    [1, 0.053, 0.0012],
    [0.7395, 0.0614, 0.0125],
    [0.0746, 0.4967, 0.4493],
    [0.6811, 0.1, 0.051],
    [0.0516, 0.5156, 0.466],
    [0.0493, 0.517, 0.4672],
    [0.0503, 0.5168, 0.4669],
    [0.0700, 0.5051, 0.457],
    [0.1301, 0.4964, 0.444],
    [0.00000001, 0.5798, 0.532],
    [0.7316, 0.6954, 0.6861],
    [0.1254, 0.6702, 0.6184],
    [0.7668, 0.3363, 0.2657],
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
