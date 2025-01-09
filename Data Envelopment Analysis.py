# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:42:50 2025

@author: C-att
"""
import numpy as np
from scipy.optimize import linprog

def dea_vrs_input(X, Y):
    """
    Performs input-oriented DEA with variable returns to scale.

    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs).
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs).

    Returns:
        A list of efficiency scores for each DMU.
    """

    n = X.shape[0]  # Number of DMUs
    m = X.shape[1]  # Number of inputs
    s = Y.shape[1]  # Number of outputs

    efficiency_scores = []

    for i in range(n):
        # Define the objective function (minimize input)
        c = X[i, :]

        # Define the inequality constraints (output constraints)
        A_ub = -np.repeat(Y[i, :].reshape(1, -1), n, axis=0)  # Reshape and repeat for all DMUs
        b_ub = -Y[i, :]

        # Define the equality constraints (input and VRS constraints)
        A_eq = np.zeros((m + 1, m + n))
        A_eq[0:m, 0:m] = np.eye(m)  # Input constraint
        A_eq[m, :] = np.ones(m + n)  # VRS constraint
        b_eq = np.hstack((X[i, :], 1))

        # Define bounds for variables (lambdas and multiplier for VRS)
        bounds = [(0, None)] * (m + n)

        # Solve the linear programming problem
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

        # Extract efficiency score
        efficiency_score = 1 / res.fun
        efficiency_scores.append(efficiency_score)

    return efficiency_scores

# Sample data (replace with your actual data)
data = {
    'DMU': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'Emissions': [-4.13863E-06, -1.25178E-06, -1.2841E-05, -9.21685E-06, -2.68238E-07, -8.43696E-06, -3.24155E-08, -1.03761E-08, -5.02843E-08, -2.62322E-07, -1.12817E-06, 6.14404E-07, -1.05822E-05, -1.53938E-06, -1.04867E-05],
    'Employment': [2.99592E-06, -5.90213E-07, -2.87891E-06, -2.82652E-06, -1.26474E-07, -2.58736E-06, -9.15524E-09, -3.54977E-10, -1.72027E-09, -7.40887E-08, -1.28036E-07, 3.89289E-07, 1.10651E-06, 9.49974E-07, -1.12141E-06],
    'Value_Added': [8.34625E-06, -1.31606E-06, -7.3013E-06, -7.12468E-06, -2.82013E-07, -6.52183E-06, -1.97862E-08, -1.02722E-09, -4.97807E-09, -1.60119E-07, -3.64994E-07, 1.01377E-06, 3.4279E-06, 2.36828E-06, -3.15749E-06]
}

# Extract input and output data
X = np.array(data['Emissions']).reshape(-1, 1)  # Assuming Emissions is the only input
Y = np.array([data['Employment'], data['Value_Added']]).T

efficiency_scores = dea_vrs_input(X, Y)
print(efficiency_scores)

#%%

import numpy as np
from scipy.optimize import linprog

def dea_vrs_input(X, Y):
    """
    Performs input-oriented DEA with variable returns to scale.

    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs).
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs).

    Returns:
        A list of efficiency scores for each DMU.
    """
    n, m = X.shape  # Number of DMUs and inputs
    _, s = Y.shape  # Number of outputs

    efficiency_scores = []

    for i in range(n):
        # Define the objective function (minimize weighted inputs for DMU `i`)
        c = np.zeros(n + 1)
        c[-1] = 1  # Minimize theta (efficiency variable)

        # Inequality constraints for outputs
        A_ub = np.hstack([-Y, np.zeros((n, 1))])
        b_ub = -Y[i]

        # Equality constraints for inputs and VRS (lambda and theta)
        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X.T
        A_eq[:m, -1] = -X[i]
        A_eq[m, :n] = 1  # Sum of lambdas = 1 (VRS constraint)
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1

        # Bounds for lambda and theta
        bounds = [(0, None)] * n + [(0, None)]  # Lambdas >= 0, theta >= 0

        # Solve the linear programming problem
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if res.success:
            efficiency_scores.append(res.x[-1])  # Efficiency score (theta)
        else:
            efficiency_scores.append(np.nan)  # Return NaN if optimization fails

    return efficiency_scores

# Sample data (replace with your actual data)
data =  { 'DMU': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'Emissions': [-4.13863E-06, -1.25178E-06, -1.2841E-05, -9.21685E-06, -2.68238E-07, 
                  -8.43696E-06, -3.24155E-08, -1.03761E-08, -5.02843E-08, -2.62322E-07, 
                  -1.12817E-06, 6.14404E-07, -1.05822E-05, -1.53938E-06, -1.04867E-05],
    'Employment': [2.99592E-06, -5.90213E-07, -2.87891E-06, -2.82652E-06, -1.26474E-07, 
                   -2.58736E-06, -9.15524E-09, -3.54977E-10, -1.72027E-09, -7.40887E-08, 
                   -1.28036E-07, 3.89289E-07, 1.10651E-06, 9.49974E-07, -1.12141E-06],
    'Value_Added': [8.34625E-06, -1.31606E-06, -7.3013E-06, -7.12468E-06, -2.82013E-07, 
                    -6.52183E-06, -1.97862E-08, -1.02722E-09, -4.97807E-09, -1.60119E-07, 
                    -3.64994E-07, 1.01377E-06, 3.4279E-06, 2.36828E-06, -3.15749E-06]
}

# Extract input and output data
X = np.array(data['Emissions']).reshape(-1, 1)  # Assuming Emissions is the only input
Y = np.array([data['Employment'], data['Value_Added']]).T

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Display results
for dmu, score in zip(data['DMU'], efficiency_scores):
    print(f"DMU {dmu}: Efficiency Score = {score}")

#%%
import numpy as np
from scipy.optimize import linprog

def dea_vrs_input(X, Y):
    """
    Performs input-oriented DEA with variable returns to scale.

    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs).
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs).

    Returns:
        A list of efficiency scores for each DMU.
    """
    n, m = X.shape  # Number of DMUs and inputs
    _, s = Y.shape  # Number of outputs

    efficiency_scores = []

    for i in range(n):
        # Define the objective function (minimize weighted inputs for DMU `i`)
        c = np.zeros(n + 1)
        c[-1] = 1  # Minimize theta (efficiency variable)

        # Inequality constraints for outputs
        A_ub = np.hstack([-Y, np.zeros((n, 1))])  # Negative Y for output-oriented constraint
        b_ub = -Y[i]  # Upper bounds for outputs

        # Equality constraints for inputs and VRS
        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X.T  # Input constraints
        A_eq[:m, -1] = -X[i]  # Efficiency (theta)
        A_eq[m, :n] = 1  # Sum of lambdas = 1 (VRS)
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1

        # Bounds for lambda and theta
        bounds = [(0, None)] * n + [(0, None)]  # Lambdas >= 0, theta >= 0

        # Solve the linear programming problem
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if res.success:
            efficiency_scores.append(res.x[-1])  # Efficiency score (theta)
        else:
            efficiency_scores.append(np.nan)  # Return NaN if optimization fails

    return efficiency_scores

# Sample data (replace with your actual data)
data = {
    'DMU': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'Emissions': [-4.13863E-06, -1.25178E-06, -1.2841E-05, -9.21685E-06, -2.68238E-07, 
                  -8.43696E-06, -3.24155E-08, -1.03761E-08, -5.02843E-08, -2.62322E-07, 
                  -1.12817E-06, 6.14404E-07, -1.05822E-05, -1.53938E-06, -1.04867E-05],
    'Employment': [2.99592E-06, -5.90213E-07, -2.87891E-06, -2.82652E-06, -1.26474E-07, 
                   -2.58736E-06, -9.15524E-09, -3.54977E-10, -1.72027E-09, -7.40887E-08, 
                   -1.28036E-07, 3.89289E-07, 1.10651E-06, 9.49974E-07, -1.12141E-06],
    'Value_Added': [8.34625E-06, -1.31606E-06, -7.3013E-06, -7.12468E-06, -2.82013E-07, 
                    -6.52183E-06, -1.97862E-08, -1.02722E-09, -4.97807E-09, -1.60119E-07, 
                    -3.64994E-07, 1.01377E-06, 3.4279E-06, 2.36828E-06, -3.15749E-06]
}

# Extract input and output data
X = np.array(data['Emissions']).reshape(-1, 1)  # Assuming Emissions is the only input
Y = np.array([data['Employment'], data['Value_Added']]).T

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Display results
for dmu, score in zip(data['DMU'], efficiency_scores):
    print(f"DMU {dmu}: Efficiency Score = {score}")

#%%
import numpy as np
from scipy.optimize import linprog

def dea_vrs_input(X, Y):
    """
    Performs input-oriented DEA with variable returns to scale.
    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs)
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs)
    Returns:
        A list of efficiency scores for each DMU
    """
    n, m = X.shape  # Number of DMUs and inputs
    _, s = Y.shape  # Number of outputs
    efficiency_scores = []
    
    for i in range(n):
        # Define the objective function (minimize theta)
        c = np.zeros(n + 1)
        c[-1] = 1
        
        # Output constraints: -Y𝜆 ≤ -y_i
        A_ub_output = np.zeros((s, n + 1))
        A_ub_output[:, :n] = -Y.T
        b_ub_output = -Y[i]
        
        # Input constraints: X𝜆 - θx_i ≤ 0
        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X.T
        A_eq[:m, -1] = -X[i]
        
        # VRS constraint: sum of lambdas = 1
        A_eq[m, :n] = 1
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1
        
        # Bounds for lambda and theta
        bounds = [(0, None)] * n + [(0, None)]
        
        # Solve the linear programming problem
        res = linprog(
            c,
            A_ub=A_ub_output,
            b_ub=b_ub_output,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )
        
        if res.success:
            efficiency_scores.append(res.x[-1])
        else:
            efficiency_scores.append(np.nan)
            print(f"Optimization failed for DMU {i+1}: {res.message}")
    
    return efficiency_scores

# Sample data
data = {
    'DMU': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'Emissions': [-4.13863E-06, -1.25178E-06, -1.2841E-05, -9.21685E-06, -2.68238E-07, 
                  -8.43696E-06, -3.24155E-08, -1.03761E-08, -5.02843E-08, -2.62322E-07, 
                  -1.12817E-06, 6.14404E-07, -1.05822E-05, -1.53938E-06, -1.04867E-05],
    'Employment': [2.99592E-06, -5.90213E-07, -2.87891E-06, -2.82652E-06, -1.26474E-07, 
                   -2.58736E-06, -9.15524E-09, -3.54977E-10, -1.72027E-09, -7.40887E-08, 
                   -1.28036E-07, 3.89289E-07, 1.10651E-06, 9.49974E-07, -1.12141E-06],
    'Value_Added': [8.34625E-06, -1.31606E-06, -7.3013E-06, -7.12468E-06, -2.82013E-07, 
                    -6.52183E-06, -1.97862E-08, -1.02722E-09, -4.97807E-09, -1.60119E-07, 
                    -3.64994E-07, 1.01377E-06, 3.4279E-06, 2.36828E-06, -3.15749E-06]
}

# Extract input and output data
X = np.array(data['Emissions']).reshape(-1, 1)  # Single input
Y = np.array([data['Employment'], data['Value_Added']]).T  # Two outputs

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Display results
for dmu, score in zip(data['DMU'], efficiency_scores):
    print(f"DMU {dmu}: Efficiency Score = {score:.4f}")
    
    #%%
import numpy as np
from scipy.optimize import linprog

def dea_vrs_input(X, Y):
    """
    Performs input-oriented DEA with variable returns to scale.
    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs)
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs)
    Returns:
        A list of efficiency scores for each DMU
    """
    n, m = X.shape  # Number of DMUs and inputs
    _, s = Y.shape  # Number of outputs
    efficiency_scores = []
    
    for i in range(n):
        # Define the objective function (minimize theta)
        c = np.zeros(n + 1)
        c[-1] = 1
        
        # Output constraints: -Y𝜆 ≤ -y_i
        A_ub_output = np.zeros((s, n + 1))
        A_ub_output[:, :n] = -Y.T
        b_ub_output = -Y[i]
        
        # Input constraints: X𝜆 - θx_i ≤ 0
        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X.T
        A_eq[:m, -1] = -X[i]
        
        # VRS constraint: sum of lambdas = 1
        A_eq[m, :n] = 1
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1
        
        # Bounds for lambda and theta
        bounds = [(0, None)] * n + [(0, None)]
        
        # Solve the linear programming problem
        res = linprog(
            c,
            A_ub=A_ub_output,
            b_ub=b_ub_output,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )
        
        if res.success:
            efficiency_scores.append(res.x[-1])
        else:
            efficiency_scores.append(np.nan)
            print(f"Optimization failed for DMU {i+1}: {res.message}")
    
    return efficiency_scores

# Sample data
data = {
    'DMU': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'Emissions': [-4.13863E-06, -1.25178E-06, -1.2841E-05, -9.21685E-06, -2.68238E-07, 
                  -8.43696E-06, -3.24155E-08, -1.03761E-08, -5.02843E-08, -2.62322E-07, 
                  -1.12817E-06, 6.14404E-07, -1.05822E-05, -1.53938E-06, -1.04867E-05],
    'Employment': [2.99592E-06, -5.90213E-07, -2.87891E-06, -2.82652E-06, -1.26474E-07, 
                   -2.58736E-06, -9.15524E-09, -3.54977E-10, -1.72027E-09, -7.40887E-08, 
                   -1.28036E-07, 3.89289E-07, 1.10651E-06, 9.49974E-07, -1.12141E-06],
    'Value_Added': [8.34625E-06, -1.31606E-06, -7.3013E-06, -7.12468E-06, -2.82013E-07, 
                    -6.52183E-06, -1.97862E-08, -1.02722E-09, -4.97807E-09, -1.60119E-07, 
                    -3.64994E-07, 1.01377E-06, 3.4279E-06, 2.36828E-06, -3.15749E-06]
}

# Ensure non-negativity
shift = abs(min(min(data['Emissions']), min(data['Employment']), min(data['Value_Added']))) + 1
data['Emissions'] = [x + shift for x in data['Emissions']]
data['Employment'] = [x + shift for x in data['Employment']]
data['Value_Added'] = [x + shift for x in data['Value_Added']]
# Normalize data to [0, 1]
max_emissions = max(data['Emissions'])
max_employment = max(data['Employment'])
max_value_added = max(data['Value_Added'])

data['Emissions'] = [x / max_emissions for x in data['Emissions']]
data['Employment'] = [x / max_employment for x in data['Employment']]
data['Value_Added'] = [x / max_value_added for x in data['Value_Added']]

# Rescale data
scale_factor = 1e6
data['Emissions'] = [x * scale_factor for x in data['Emissions']]
data['Employment'] = [x * scale_factor for x in data['Employment']]
data['Value_Added'] = [x * scale_factor for x in data['Value_Added']]

# Extract input and output data
X = np.array(data['Emissions']).reshape(-1, 1)  # Single input
Y = np.array([data['Employment'], data['Value_Added']]).T  # Two outputs

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Display results
for dmu, score in zip(data['DMU'], efficiency_scores):
    print(f"DMU {dmu}: Efficiency Score = {score:.4f}")

#%% DEA with proportional normalization 

import numpy as np
from scipy.optimize import linprog

def normalize_column(column):
    """
    Normalize a column to ensure non-negativity and scale to [0, 1].
    """
    min_val = min(column)
    shift = abs(min_val) + 1  # Ensure non-negativity
    shifted_column = [x + shift for x in column]
    max_val = max(shifted_column)
    normalized_column = [x / max_val for x in shifted_column]
    return normalized_column



def dea_vrs_input(X, Y):
    """
    Performs input-oriented DEA with variable returns to scale.
    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs)
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs)
    Returns:
        A list of efficiency scores for each DMU
    """
    n, m = X.shape  # Number of DMUs and inputs
    _, s = Y.shape  # Number of outputs
    efficiency_scores = []
    
    for i in range(n):
        # Define the objective function (minimize theta)
        c = np.zeros(n + 1)
        c[-1] = 1
        
        # Output constraints: -Y𝜆 ≤ -y_i
        A_ub_output = np.zeros((s, n + 1))
        A_ub_output[:, :n] = -Y.T
        b_ub_output = -Y[i]
        
        # Input constraints: X𝜆 - θx_i ≤ 0
        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X.T
        A_eq[:m, -1] = -X[i]
        
        # VRS constraint: sum of lambdas = 1
        A_eq[m, :n] = 1
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1
        
        # Bounds for lambda and theta
        bounds = [(0, None)] * n + [(0, None)]
        
        # Solve the linear programming problem
        res = linprog(
            c,
            A_ub=A_ub_output,
            b_ub=b_ub_output,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )
        
        if res.success:
            efficiency_scores.append(res.x[-1])
        else:
            efficiency_scores.append(np.nan)
            print(f"Optimization failed for DMU {i+1}: {res.message}")
    
    return efficiency_scores



def validate_data(X, Y):
    if X.size == 0 or Y.size == 0:
        raise ValueError("Empty input/output matrices")
    if np.any(np.isnan(X)) or np.any(np.isnan(Y)):
        raise ValueError("Input contains NaN values")
    if X.shape[0] != Y.shape[0]:
        raise ValueError("Inconsistent number of DMUs")

# Original data
data = {
    "Delta_E": [-117423057.3, -35516080.36, -364330667.9, -261504734.9, -7610589.044, 
                -239377416.2, -919707.8518, -294396.2818, -1426689.687, -7442722.482, 
                -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5],
    "Delta_Emp": [9.114687303, -1.795646081, -8.75869875, -8.59932818, -0.384781324, 
                  -7.871692884, -0.02785362, -0.001079969, -0.005233698, -0.225405011, 
                  -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282],
    "Delta_VA": [441.8022859, -69.66453618, -386.48829, -377.1394629, -14.92811568, 
                 -345.2276694, -1.047364889, -0.054375153, -0.263510378, -8.475785146, 
                 -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149]
}

# Normalize data
normalized_data = {key: normalize_column(values) for key, values in data.items()}

# Extract input and output data
X = np.array(normalized_data['Delta_E']).reshape(-1, 1)  # Single input
Y = np.array([normalized_data['Delta_Emp'], normalized_data['Delta_VA']]).T  # Two outputs

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Display results
for dmu, score in enumerate(efficiency_scores, start=1):
    print(f"DMU {dmu}: Efficiency Score = {score:.4f}")
    
#%%
import numpy as np
from scipy.optimize import linprog

def normalize_column(column):
    """
    Normalize a column to ensure non-negativity and scale to [0, 1].
    """
    min_val = min(column)
    shift = abs(min_val) + 1  # Ensure non-negativity
    shifted_column = [x + shift for x in column]
    max_val = max(shifted_column)
    normalized_column = [x / max_val for x in shifted_column]
    return normalized_column

def dea_vrs_input_weighted(X, Y, input_weights, output_weights):
    """
    Performs weighted input-oriented DEA with variable returns to scale.
    Args:
        X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs)
        Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs)
        input_weights: Weights for input variables (array of length m)
        output_weights: Weights for output variables (array of length s)
    Returns:
        A list of efficiency scores for each DMU
    """
    n, m = X.shape  # Number of DMUs and inputs
    _, s = Y.shape  # Number of outputs
    
    # Apply weights to input and output matrices
    X_weighted = X * input_weights
    Y_weighted = Y * output_weights
    
    efficiency_scores = []
    
    for i in range(n):
        # Define the objective function (minimize theta)
        c = np.zeros(n + 1)
        c[-1] = 1
        
        # Output constraints: -Y𝜆 ≤ -y_i (with weights)
        A_ub_output = np.zeros((s, n + 1))
        A_ub_output[:, :n] = -Y_weighted.T
        b_ub_output = -Y_weighted[i]
        
        # Input constraints: X𝜆 - θx_i ≤ 0 (with weights)
        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X_weighted.T
        A_eq[:m, -1] = -X_weighted[i]
        
        # VRS constraint: sum of lambdas = 1
        A_eq[m, :n] = 1
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1
        
        # Bounds for lambda and theta
        bounds = [(0, None)] * n + [(0, None)]
        
        # Solve the linear programming problem
        res = linprog(
            c,
            A_ub=A_ub_output,
            b_ub=b_ub_output,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )
        
        if res.success:
            efficiency_scores.append(res.x[-1])
        else:
            efficiency_scores.append(np.nan)
            print(f"Optimization failed for DMU {i+1}: {res.message}")
    
    return efficiency_scores

# Original data
data = {
    "Delta_E": [-117423057.3, -35516080.36, -364330667.9, -261504734.9, -7610589.044, 
                -239377416.2, -919707.8518, -294396.2818, -1426689.687, -7442722.482, 
                -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5],
    "Delta_Emp": [9.114687303, -1.795646081, -8.75869875, -8.59932818, -0.384781324, 
                  -7.871692884, -0.02785362, -0.001079969, -0.005233698, -0.225405011, 
                  -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282],
    "Delta_VA": [441.8022859, -69.66453618, -386.48829, -377.1394629, -14.92811568, 
                 -345.2276694, -1.047364889, -0.054375153, -0.263510378, -8.475785146, 
                 -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149]
}

# Normalize data
normalized_data = {key: normalize_column(values) for key, values in data.items()}

# Extract input and output data
X = np.array(normalized_data['Delta_E']).reshape(-1, 1)  # Single input
Y = np.array([normalized_data['Delta_Emp'], normalized_data['Delta_VA']]).T  # Two outputs

# Define weights
input_weights = np.array([0.5])  # Weight for Delta_E
output_weights = np.array([0.25, 0.25])  # Weights for Delta_Emp and Delta_VA

# Calculate efficiency scores with weights
efficiency_scores = dea_vrs_input_weighted(X, Y, input_weights, output_weights)

# Display results
print("\nWeighted DEA Results:")
print("Input weight (Delta_E):", input_weights[0])
print("Output weights (Delta_Emp, Delta_VA):", output_weights[0], output_weights[1])
print("\nEfficiency Scores:")
for dmu, score in enumerate(efficiency_scores, start=1):
    print(f"DMU {dmu}: Efficiency Score = {score:.4f}")

#%%
from scipy.stats import zscore

def rescale_efficiency(scores, new_min=0.5, new_max=1.0):
    old_min, old_max = min(scores), max(scores)
    return [(new_min + (score - old_min) * (new_max - new_min) / (old_max - old_min)) for score in scores]


# Apply Z-score normalization
data_zscore = {key: zscore(values) for key, values in data.items()}

# Convert to positive range (shift to avoid negative values)
data_shifted = {key: [x - min(data_zscore[key]) + 1 for x in values] for key, values in data_zscore.items()}

# Use normalized data for DEA
X = np.array(data_shifted['Delta_E']).reshape(-1, 1)
Y = np.array([data_shifted['Delta_Emp'], data_shifted['Delta_VA']]).T

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Rescale scores for closer values
efficiency_scores_rescaled = rescale_efficiency(efficiency_scores, new_min=0.5, new_max=1.0)

# Display results
for dmu, score in enumerate(efficiency_scores_rescaled, start=1):
    print(f"DMU {dmu}: Rescaled Efficiency Score = {score:.4f}")
#%% 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

normalized_data = [
    [0.5881, 0.8000, 0.8000],
    [0.7168, 0.4337, 0.4295],
    [0.2000, 0.2000, 0.2000],
    [0.3616, 0.2054, 0.2068],
    [0.7606, 0.4811, 0.4692],
    [0.3964, 0.2298, 0.2299],
    [0.7712, 0.4931, 0.4792],
    [0.7721, 0.4940, 0.4799],
    [0.7704, 0.4938, 0.4798],
    [0.7609, 0.4865, 0.4738],
    [0.7223, 0.4810, 0.4660],
    [0.8000, 0.5338, 0.5188],
    [0.3007, 0.6070, 0.6114],
    [0.7040, 0.5910, 0.5708],
    [0.3050, 0.3795, 0.3589],
]

columns = ["Delta_E", "Delta_Emp", "Delta_VA"]
DMUs = [f"DMU {i}" for i in range(1, len(normalized_data) + 1)]
df = pd.DataFrame(normalized_data, columns=columns, index=DMUs)

def create_color_array(data, reverse_first_column=True):
    colors = ['#ef5350', '#ffffff', '#42a5f5']  # Red to white to blue
    custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
    
    normalized = np.zeros_like(data)
    for i in range(data.shape[1]):
        if i == 0 and reverse_first_column:  # Delta_E column
            normalized[:, i] = (data.iloc[:, i].max() - data.iloc[:, i]) / (data.iloc[:, i].max() - data.iloc[:, i].min())
        else:  # Other columns
            normalized[:, i] = (data.iloc[:, i] - 0.2) / (1.0 - 0.2)
    
    return custom_cmap(normalized)

fig, ax = plt.subplots(figsize=(7, 4))
ax.axis('tight')
ax.axis('off')

cell_colors = create_color_array(df)

table = ax.table(
    cellText=df.round(4).values,
    rowLabels=df.index,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    cellColours=cell_colors
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(columns) + 1)))

for i in range(len(columns)):
    table[(0, i)].set_facecolor('#455a64')
    table[(0, i)].set_text_props(color='white', weight='bold')

for i in range(len(DMUs)):
    table[(i + 1, -1)].set_facecolor('#546e7a')
    table[(i + 1, -1)].set_text_props(color='white', weight='bold')

for cell in table._cells:
    table._cells[cell].set_edgecolor('#bdbdbd')
    table._cells[cell].set_linewidth(1)

plt.title("DEA Normalized Data Analysis", pad=20, fontsize=14, weight='bold')
plt.figtext(0.99, 0.01, 'Delta_E: 0.8 (red) → 0.2 (blue)\nOther metrics: 0.2 (red) → 1.0 (blue)', 
            ha='right', va='bottom', fontsize=8, style='italic')

plt.tight_layout()
plt.show()


#%%


# Normalization Range: The data is normalized to a range of 
# [0.2,0.8] [0.2,0.8], which reduces the impact of extreme values and brings the efficiency scores closer to each other.
# DEA Scores: The DEA model uses the normalized data, leading to a more balanced distribution of efficiency scores.
# Method: Data is scaled to fit a tighter range 
# [0.2,0.8],[0.2,0.8], effectively limiting the influence of extreme values.
# Outcome Characteristics:
# Scores are closer together, and no DMU scores below 0.2 or above 1.0.
# Intermediate DMUs (e.g., DMUs 4–15) show less disparity in scores compared to proportional normalization.
# DMUs 1, 3, and 13 maintain scores of 1.000 but other DMUs score closer to each other.
# Reason: Adjusting the range limits the influence of outliers while preserving relative differences. By compressing the scale, efficiency scores are less spread out, which reduces large discrepancies between DMUs.
# Conclusion: This method moderates variability while maintaining interpretability, making it ideal for visual comparisons or if extreme variability is undesirable.

import numpy as np
from scipy.optimize import linprog

def dea_vrs_input(X, Y):
    n, m = X.shape
    _, s = Y.shape
    efficiency_scores = []
    
    for i in range(n):
        c = np.zeros(n + 1)
        c[-1] = 1

        A_ub_output = np.zeros((s, n + 1))
        A_ub_output[:, :n] = -Y.T
        b_ub_output = -Y[i]

        A_eq = np.zeros((m + 1, n + 1))
        A_eq[:m, :n] = X.T
        A_eq[:m, -1] = -X[i]

        A_eq[m, :n] = 1
        b_eq = np.zeros(m + 1)
        b_eq[m] = 1

        bounds = [(0, None)] * n + [(0, None)]

        res = linprog(
            c,
            A_ub=A_ub_output,
            b_ub=b_ub_output,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )
        
        if res.success:
            efficiency_scores.append(res.x[-1])
        else:
            efficiency_scores.append(np.nan)
            print(f"Optimization failed for DMU {i+1}: {res.message}")
    
    return efficiency_scores

# Min-max normalization function
def min_max_normalize(data, new_min=0.2, new_max=0.8):
    old_min, old_max = min(data), max(data)
    return [(new_min + (x - old_min) * (new_max - new_min) / (old_max - old_min)) for x in data]

# Sample data
data = {
    'Delta_E': [-117423057.3, -35516080.36, -364330667.9, -261504734.9, -7610589.044,
                -239377416.2, -919707.8518, -294396.2818, -1426689.687, -7442722.482,
                -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5],
    'Delta_Emp': [9.114687303, -1.795646081, -8.75869875, -8.59932818, -0.384781324,
                  -7.871692884, -0.02785362, -0.001079969, -0.005233698, -0.225405011,
                  -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282],
    'Delta_VA': [441.8022859, -69.66453618, -386.48829, -377.1394629, -14.92811568,
                 -345.2276694, -1.047364889, -0.054375153, -0.263510378, -8.475785146,
                 -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149]
}

# Normalize data
normalized_data = {
    key: min_max_normalize(values, new_min=0.2, new_max=0.8) for key, values in data.items()
}

# Convert normalized data into input/output arrays
X = np.array(normalized_data['Delta_E']).reshape(-1, 1)
Y = np.array([normalized_data['Delta_Emp'], normalized_data['Delta_VA']]).T

# Calculate efficiency scores
efficiency_scores = dea_vrs_input(X, Y)

# Display results
for dmu, score in enumerate(efficiency_scores, start=1):
    print(f"DMU {dmu}: Efficiency Score = {score:.4f}")
# #%%
# import numpy as np
# from scipy.optimize import linprog

# def normalize_column(column):
#     """
#     Normalize a column to ensure non-negativity and scale to [0, 1].
#     """
#     min_val = min(column)
#     shift = abs(min_val) + 1  # Ensure non-negativity
#     shifted_column = [x + shift for x in column]
#     max_val = max(shifted_column)
#     normalized_column = [x / max_val for x in shifted_column]
#     return normalized_column

# def dea_vrs_input_weighted(X, Y, weights):
#     """
#     Performs input-oriented DEA with variable returns to scale and weighted inputs.
#     Args:
#         X: Input matrix (n x m, where n is the number of DMUs and m is the number of inputs)
#         Y: Output matrix (n x s, where n is the number of DMUs and s is the number of outputs)
#         weights: List of weights for each input.
#     Returns:
#         A list of efficiency scores for each DMU
#     """
#     n, m = X.shape  # Number of DMUs and inputs
#     _, s = Y.shape  # Number of outputs
#     efficiency_scores = []

#     for i in range(n):
#         # Define the objective function (minimize theta)
#         c = np.zeros(n + 1)
#         c[-1] = 1

#         # Output constraints: -Y𝜆 ≤ -y_i
#         A_ub_output = np.zeros((s, n + 1))
#         A_ub_output[:, :n] = -Y.T
#         b_ub_output = -Y[i]

#         # Input constraints: sum(weights * X𝜆) - θ * sum(weights * x_i) ≤ 0
#         A_eq = np.zeros((m + 1, n + 1))
#         for j in range(m):
#             A_eq[j, :n] = weights[j] * X.T[:, j] 
#         A_eq[:m, -1] = -np.sum(weights * X[i], axis=0) 

#         # VRS constraint: sum of lambdas = 1
#         A_eq[m, :n] = 1
#         b_eq = np.zeros(m + 1)
#         b_eq[m] = 1

#         # Bounds for lambda and theta
#         bounds = [(0, None)] * n + [(0, None)]

#         # Solve the linear programming problem
#         res = linprog(
#             c,
#             A_ub=A_ub_output,
#             b_ub=b_ub_output,
#             A_eq=A_eq,
#             b_eq=b_eq,
#             bounds=bounds,
#             method='highs'
#         )

#         if res.success:
#             efficiency_scores.append(res.x[-1])
#         else:
#             efficiency_scores.append(np.nan)
#             print(f"Optimization failed for DMU {i+1}: {res.message}")

#     return efficiency_scores

# # Original data
# data = {
#     "Delta_E": [-117423057.3, -35516080.36, -364330667.9, -261504734.9, -7610589.044,
#                 -239377416.2, -919707.8518, -294396.2818, -1426689.687, -7442722.482,
#                 -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5],
#     "Delta_Emp": [9.114687303, -1.795646081, -8.75869875, -8.59932818, -0.384781324,
#                   -7.871692884, -0.02785362, -0.001079969, -0.005233698, -0.225405011,
#                   -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282],
#     "Delta_VA": [441.8022859, -69.66453618, -386.48829, -377.1394629, -14.92811568,
#                   -345.2276694, -1.047364889, -0.054375153, -0.263510378, -8.475785146,
#                   -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149]
# }

# # Normalize data
# normalized_data = {key: normalize_column(values) for key, values in data.items()}

# # Extract input and output data
# X = np.array([normalized_data['Delta_E']]).T  # Single input (note the transpose for correct shape)
# Y = np.array([normalized_data['Delta_Emp'], normalized_data['Delta_VA']]).T  # Two outputs

# # Define weights
# weights = np.array([0.5]) 

# # Calculate efficiency scores
# efficiency_scores = dea_vrs_input_weighted(X, Y, weights)

# # Display results
# for dmu, score in enumerate(efficiency_scores, start=1):
#     print(f"DMU {dmu}: Efficiency Score = {score:.4f}")
