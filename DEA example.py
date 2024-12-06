import itertools
import pandas as pd
import numpy as np
from pyDEA.core.models.bound_generator import create_automatic_bounds
from pyDEA.core.data_processing.input_output_data import convert_to_dictionary
from pyDEA.core.models.basic_model import DEAProblem
from pyDEA.core.utils.dea_utils import add_efficiency_column

# Seed for reproducibility
np.random.seed(42)

# Define 15 interventions
interventions = [
    "Material Recycling", "Modular Construction", "Renewable Energy Usage",
    "On-Site Waste Recovery", "Extended Product Lifespan", "Material Substitution",
    "Digital Tools (BIM)", "Pre-fabrication", "Urban Mining", "Eco-design",
    "Closed-Loop Supply Chains", "Shared Equipment Leasing", "Low-Carbon Logistics",
    "Green Procurement", "Renewable Insulation"
]

# Generate random baseline data
data = {
    "Intervention": interventions,
    "GHG Emissions (Input)": np.random.uniform(50, 100, size=15),
    "Value Added (Output 1)": np.random.uniform(1000, 2000, size=15),
    "Employment (Output 2)": np.random.uniform(10000, 20000, size=15),
}

# Create a DataFrame
df = pd.DataFrame(data)

# Helper function to calculate DEA efficiency
def calculate_dea_efficiency(inputs, outputs):
    data_dict = convert_to_dictionary(
        inputs=inputs,
        outputs=outputs,
        orientation="output",
        returns="VRS"
    )
    bounds = create_automatic_bounds(data_dict)
    dea_model = DEAProblem(data_dict, bounds)
    dea_model.solve()
    add_efficiency_column(data_dict, dea_model)
    return [data_dict[dm]["efficiency"] for dm in data_dict]

# Calculate baseline efficiency
df["Baseline Efficiency"] = calculate_dea_efficiency(
    inputs=df[["GHG Emissions (Input)"]],
    outputs=df[["Value Added (Output 1)", "Employment (Output 2)"]]
)

# Generate all combinations of three interventions
combinations = list(itertools.combinations(df["Intervention"], 3))

# Evaluate efficiency for each combination
results = []
for comb in combinations:
    selected = df[df["Intervention"].isin(comb)]
    avg_efficiency = selected["Baseline Efficiency"].mean()
    results.append({"Combination": comb, "Average Efficiency": avg_efficiency})

# Create a DataFrame with results
results_df = pd.DataFrame(results)

# Find the top combination
top_combination = results_df.sort_values(by="Average Efficiency", ascending=False).iloc[0]

# Print the results
print(f"Top Combination: {top_combination['Combination']}")
print(f"Average Efficiency: {top_combination['Average Efficiency']:.4f}")
