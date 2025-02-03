# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 14:06:05 2025

@author: Gebruiker
"""
#%% First the data had to be normalized by using min-max normalization and to 
# make the data non-negative a shift had to be incorperated. 
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

# Min-max normalization, using a shift to make the data non-negative and an inverse for emissions for comparability 
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
#%% Here the data will be incorperated with a more visual attractive tabel 
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

# Min-max normalization, using a shift to make the data non-negative and an inverse for emissions for comparability 
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

#%% This is a conventional weights DEA-WEI (output only) 
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
    


#%% Conventional DEA + visualization 
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

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


# DMU names
dmus = [
    '1. Steel Modular Design', '2. Steel Scrap Diversion', '3. Steel Improved yield',
    '4. Steel Weight Optimization', '5. Steel Rebar waste into nails', '6. Steel 3D printing',
    '7. Aluminium Plastic deformation', '8. Aluminium Pyrolysis recycling',
    '9. Aluminium Design for disassembly', '10. Aluminium Optimize facade designs',
    '11. Concrete Recycled Aggregate', '12. Concrete Reuse cement slag',
    '13. Concrete 3D printing', '14. Concrete Sustainable Concrete',
    '15. Concrete Fly-ash as recycled cement'
]

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
    efficiency_scores.append((dmus[i], efficiency))

# Sort efficiency scores in descending order
efficiency_scores.sort(key=lambda x: x[1], reverse=True)

# Prepare table data
table_data = [["DMU", "Efficiency Score"]] + [[label, f"{score:.3f}"] for label, score in efficiency_scores]

# Plot the table
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")

# Create the table
table = ax.table(cellText=table_data, colLabels=None, loc='center', cellLoc='center')

# Style the header row
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#e6e6e6')  # Light grey for headers
        cell.set_text_props(weight="bold")  # Bold header text
    elif row > 0:  # Data rows
        # Highlight cells based on efficiency values
        if col == 1:  # Efficiency Score column
            value = float(cell.get_text().get_text())
            if value > 0.85:
                cell.set_facecolor('lightgreen')  # Green for high values
            elif value < 0.5:
                cell.set_facecolor('lightcoral')  # Red for low values
        elif row % 2 == 1:  # Alternate row colors
            cell.set_facecolor('#f9f9f9')

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.1, 1.2)

# Add a title
plt.title("Efficiency Scores of DMUs (Descending Order)", fontsize=14, pad=10)

# Adjust the layout
plt.tight_layout()

# Show the plot
plt.show()

#%% Common weights DEA 
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

# Common weights, no maximization of the best indicator
weights = np.array([0.33, 0.33, 0.33])  # Adjust based on preference or domain knowledge

# Check normalization
weights = weights / weights.sum()

# DEA for each DMU
for i in range(n_dmus):
    # Target DMU's outputs
    y_o = Y[i]
    
    # Objective function (maximize weighted outputs for DMU i)
    # Use fixed weights directly for evaluation
    efficiency = np.dot(weights, y_o)
    
    # Constraints (outputs of all DMUs ≤ 1 under the same weights)
    A = np.dot(Y, weights)
    b = np.ones(n_dmus)
    
    # Efficiency score is scaled to check feasibility
    efficiency_score = efficiency / max(A)
    efficiency_scores.append(efficiency_score)

# Print results
for i, score in enumerate(efficiency_scores):
    print(f"Efficiency of DMU{i+1}: {score:.4f}")
    
#%% Common weights + visualization 
import numpy as np
import matplotlib.pyplot as plt

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

# DMU names
dmus = [
    '1. Steel Modular Design', '2. Steel Scrap Diversion', '3. Steel Improved yield',
    '4. Steel Weight Optimization', '5. Steel Rebar waste into nails', '6. Steel 3D printing',
    '7. Aluminium Plastic deformation', '8. Aluminium Pyrolysis recycling',
    '9. Aluminium Design for disassembly', '10. Aluminium Optimize facade designs',
    '11. Concrete Recycled Aggregate', '12. Concrete Reuse cement slag',
    '13. Concrete 3D printing', '14. Concrete Sustainable Concrete',
    '15. Concrete Fly-ash as recycled cement'
]

n_dmus, n_outputs = Y.shape

# Common Weights DEA
def common_weights_dea(Y):
    # Equal weights across outputs
    weights = np.array([1/3, 1/3, 1/3])
    
    efficiency_scores = []
    for i in range(n_dmus):
        # Calculate efficiency using fixed weights
        efficiency = np.dot(weights, Y[i])
        
        # Normalize by maximum weighted sum
        max_weighted_sum = np.max(np.dot(Y, weights))
        efficiency_score = efficiency / max_weighted_sum
        
        efficiency_scores.append(efficiency_score)
    
    return efficiency_scores

# Calculate common weights efficiency scores
common_scores = common_weights_dea(Y)

# Combine DMUs with their scores and sort
efficiency_ranking = sorted(zip(dmus, common_scores), key=lambda x: x[1], reverse=True)

# Plot results
plt.figure(figsize=(10, 6))
plt.axis("off")

# Prepare table data
table_data = [
    ["DMU", "Common Weights\nEfficiency Score",]
] + [
    [label, f"{score:.3f}"] for label, score in efficiency_ranking
]

# Create table
table = plt.table(
    cellText=table_data, 
    loc='center', 
    cellLoc='center',
    colWidths=[0.4, 0.4]  # Adjust column widths
)

# Style the table
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#e6e6e6')
        cell.set_text_props(weight="bold")
        cell.get_text().set_linespacing(0.9)  # Adjust line spacing
        cell.get_text().set_verticalalignment('center')
        cell.set_height(0.05)
    elif col == 1:  # Efficiency score column
        value = float(cell.get_text().get_text())
        if value > 0.85:
            cell.set_facecolor('lightgreen')
        elif value < 0.42:
            cell.set_facecolor('lightcoral')
        elif row % 2 == 1:
            cell.set_facecolor('#f9f9f9')

# Table styling
table.auto_set_font_size(False)
table.set_fontsize(9)  # Slightly smaller font
plt.subplots_adjust(bottom=0.1)  # Increase bottom margin if needed
table.scale(1.1, 1.2)

# Title
plt.title("Common Weights DEA Efficiency score", fontsize=14, pad=2)

plt.tight_layout()
plt.show()

# Print top 3 efficient DMUs
print("\nTop 3 Efficient DMUs:")
for dmu, score in efficiency_ranking[:3]:
    print(f"{dmu}: {score:.3f}")
#%% Priority analysis of common weights: Medium Priority 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create the data
data = {
    'DMUs': [
        '1. Steel Modular Design', '2. Steel Scrap Diversion', '3. Steel Improved yield',
        '4. Steel Weight Optimization', '5. Steel Rebar waste into nails', '6. Steel 3D printing',
        '7. Aluminium Plastic deformation', '8. Aluminium Pyrolysis recycling',
        '9. Aluminium Design for disassembly', '10. Aluminium Optimize facade designs',
        '11. Concrete Recycled Aggregate', '12. Concrete Reuse cement slag',
        '13. Concrete 3D printing', '14. Concrete Sustainable Concrete',
        '15. Concrete Fly-ash as recycled cement'
    ],
    'M priority Emissions': [0.9386, 0.4013, 0.7221, 0.5459, 0.3850, 0.5319, 0.3813 , 0.3806, 0.3812, 0.3874, 0.4220, 0.3908, 1, 0.5411, 0.7507],
    'M priority Employment': [1, 0.4184, 0.3320, 0.2623, 0.4550, 0.2795, 0.4644, 0.4649, 0.4650, 0.4609, 0.4698, 0.5072, 0.8421, 0.6249, 0.5113],
    'M priority Value Added': [1, 0.4068, 0.3165, 0.2476, 0.4407, 0.2648, 0.4495, 0.4500, 0.4500, 0.4465, 0.4541, 0.4929, 0.8393, 0.6094, 0.4901]
}

def create_table_plot(data):
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Define the desired order
    desired_order = [1, 13, 14, 15, 12, 11, 3, 9, 8, 7, 10, 5, 2, 6, 4]
    
    # Extract number from DMUs and create sort key
    def get_sort_position(dmu_str):
        # Extract the number from the start of the string
        num = int(dmu_str.split('.')[0])
        # Find its position in desired_order (0-based index)
        return desired_order.index(num)
    
    # Add sort key and sort
    df['sort_key'] = df['DMUs'].apply(get_sort_position)
    df = df.sort_values('sort_key')
    df = df.drop('sort_key', axis=1)
    
    # Format numeric columns to 3 decimals
    df = df.round(3)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Create the table
    table = ax.table(cellText=df.values,
                    colLabels=df.columns,
                    loc='center',
                    cellLoc='center')
    
    # Style the header row (grey background)
    for j, key in enumerate(df.columns):
        cell = table[0, j]
        cell.set_facecolor('#e6e6e6')  # Light grey color
        cell.set_text_props(weight='bold')
    
    # Set cell colors based on values
    for i in range(len(df)):
        for j in range(1, 4):  # Skip the DMUs column
            cell = table[i+1, j]
            value = float(cell.get_text().get_text())
            if value >= 0.850:
                cell.set_facecolor('lightgreen')
            elif value <= 0.400:
                cell.set_facecolor('lightcoral')
            else:
                cell.set_facecolor('white')
    
    # Adjust table style
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.3)
    
    # Add title
    plt.title('DEA Medium Priority results', pad=20)
    
    plt.tight_layout()
    return plt

# Create and show the plot
plot = create_table_plot(data)
plot.show()

#%% Priority analysis of common weights: High priority 
import pandas as pd
import matplotlib.pyplot as plt

# Updated data for High Priority
data = {
    'DMUs': [
        '1. Steel Modular Design', '2. Steel Scrap Diversion', '3. Steel Improved yield', '4. Steel Weight Optimization', 
        '5. Steel Rebar waste into nails', '6. Steel 3D printing', '7. Aluminium Plastic deformation', 
        '8. Aluminium Pyrolysis recycling', '9. Aluminium Design for disassembly', '10. Aluminium Optimize facade designs', 
        '11. Concrete Recycled Aggregate', '12. Concrete Reuse cement slag', '13. Concrete 3D printing', 
        '14. Sustainable Concrete', '15. Concrete Fly-ash as recycled cement'
    ],
    'H priority Emissions': [0.5811, 0.2671, 1, 0.7437, 0.1916, 0.6953, 
                             0.1731, 0.1712, 0.1721, 0.189, 0.246, 0.138, 
                             0.8982, 0.2845, 0.8364],
    'H priority Employment': [1, 0.4206, 0.1527, 0.1332, 0.4818, 0.1641, 
                               0.4973, 0.4984, 0.4983, 0.4893, 0.4869, 0.5539, 
                               0.7478, 0.654, 0.3988],
    'H priority Value Added': [1, 0.3916, 0.1138, 0.0965, 0.4462, 0.1274, 
                               0.4601, 0.461, 0.4609, 0.4533, 0.4476, 0.518, 
                               0.7408, 0.6152, 0.3459]
}

def create_table_plot(data):
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Define the desired order
    desired_order = [1, 13, 14, 15, 12, 11, 3, 9, 8, 7, 10, 5, 2, 6, 4]
    
    # Extract number from DMUs and create sort key
    def get_sort_position(dmu_str):
        # Extract the number from the start of the string
        num = int(dmu_str.split('.')[0])
        # Find its position in desired_order (0-based index)
        return desired_order.index(num)
    
    # Add sort key and sort
    df['sort_key'] = df['DMUs'].apply(get_sort_position)
    df = df.sort_values('sort_key')
    df = df.drop('sort_key', axis=1)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    # Format numeric columns to 3 decimals
    df = df.round(3)
    # Create the table
    table = ax.table(cellText=df.values,
                    colLabels=df.columns,
                    loc='center',
                    cellLoc='center')
    
    # Style the header row (grey background)
    for j, key in enumerate(df.columns):
        cell = table[0, j]
        cell.set_facecolor('#e6e6e6')  # Light grey color
        cell.set_text_props(weight='bold')
    
    # Set cell colors based on values
    for i in range(len(df)):
        for j in range(1, 4):  # Skip the DMUs column
            cell = table[i+1, j]
            value = float(cell.get_text().get_text())
            if value >= 0.850:
                cell.set_facecolor('lightgreen')
            elif value <= 0.400:
                cell.set_facecolor('lightcoral')
            else:
                cell.set_facecolor('white')
    
    # Adjust table style
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.3)
    
    # Add title
    plt.title('DEA High Priority Results', pad=20)
    
    plt.tight_layout()
    return plt

# Create and show the plot
plot = create_table_plot(data)
plot.show()

#%% Optional: DEA with both conventional and common weights 
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

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

# DMU names
dmus = [
    '1. Steel Modular Design', '2. Steel Scrap Diversion', '3. Steel Improved yield',
    '4. Steel Weight Optimization', '5. Steel Rebar waste into nails', '6. Steel 3D printing',
    '7. Aluminium Plastic deformation', '8. Aluminium Pyrolysis recycling',
    '9. Aluminium Design for disassembly', '10. Aluminium Optimize facade designs',
    '11. Concrete Recycled Aggregate', '12. Concrete Reuse cement slag',
    '13. Concrete 3D printing', '14. Concrete Sustainable Concrete',
    '15. Concrete Fly-ash as recycled cement'
]

n_dmus, n_outputs = Y.shape

# Variable Weights DEA
def variable_weights_dea(Y):
    efficiency_scores = []
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
    
    return efficiency_scores

# Common Weights DEA
def common_weights_dea(Y):
    # Common weights, equal importance
    weights = np.array([1/3, 1/3, 1/3])
    
    efficiency_scores = []
    for i in range(n_dmus):
        # Calculate efficiency using fixed weights
        efficiency = np.dot(weights, Y[i])
        
        # Normalize by maximum weighted sum
        max_weighted_sum = np.max(np.dot(Y, weights))
        efficiency_score = efficiency / max_weighted_sum
        
        efficiency_scores.append(efficiency_score)
    
    return efficiency_scores

# Calculate efficiency scores
variable_scores = variable_weights_dea(Y)
common_scores = common_weights_dea(Y)

# Combine and sort by variable weights efficiency
combined_scores = list(zip(dmus, variable_scores, common_scores))
combined_scores.sort(key=lambda x: x[1], reverse=True)

# Prepare table data
table_data = [
    ["DMU", "Variable Weights\nEfficiency", "Common Weights\nEfficiency"]
] + [
    [label, f"{var_score:.3f}", f"{common_score:.3f}"] 
    for label, var_score, common_score in combined_scores
]

# Plot the table
plt.figure(figsize=(14, 8))
plt.axis("off")

# Create the table
table = plt.table(
    cellText=table_data, 
    loc='center', 
    cellLoc='center',
    colWidths=[0.4, 0.3, 0.3]
)

# Style the table
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#e6e6e6')  # Light grey for headers
        cell.set_text_props(weight="bold")  # Bold header text
    elif row > 0:  # Data rows
        # Highlight cells based on efficiency values
        if col == 1:  # Variable Weights Efficiency
            value = float(cell.get_text().get_text())
            if value > 0.85:
                cell.set_facecolor('lightgreen')  # Green for high values
            elif value < 0.5:
                cell.set_facecolor('lightcoral')  # Red for low values
        elif col == 2:  # Common Weights Efficiency
            value = float(cell.get_text().get_text())
            if value > 0.85:
                cell.set_facecolor('lightgreen')  # Green for high values
            elif value < 0.42:
                cell.set_facecolor('lightcoral')  # Red for low values
        elif row % 2 == 1:  # Alternate row colors
            cell.set_facecolor('#f9f9f9')

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.1, 1.2)

# Add a title
plt.title("DEA Efficiency Scores: Variable vs Common Weights", fontsize=14, pad=10)

# Adjust the layout
plt.tight_layout()

# Show the plot
plt.show()

# Print key insights
print("\nKey Insights:")
for label, var_score, common_score in combined_scores[:3]:
    print(f"{label}: Variable Weights {var_score:.3f}, Common Weights {common_score:.3f}")