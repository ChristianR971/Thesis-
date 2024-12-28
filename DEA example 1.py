import pandas as pd
from pyDEA.main import run_dea

# Input data (placeholder: 1 for each intervention since input data is not provided)
inputs = [1] * 15

# Output data (3 outputs: CO2 reductions, employment impact, and value added)
co2_reductions = [
    -117423057.3, -35516080.36, -364330667.9, -261504734.9, -7610589.044,
    -239377416.2, -3455549.736, -294396.2818, -1426689.687, -7442722.482,
    -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5
]
employment_impacts = [
    9114.687303, -1795.646081, -8758.69875, -8103.213209, -3847.812739,
    -7871.692884, 1852.65913, 29.11293018, -5.233697598, -225.4050111,
    -389.5320335, 1184.360868, 3366.41353, 2890.169701, -3411.73282
]
value_added = [
    441802285.9, -69664536.18, -386488290, -355381422, -149281137.6,
    -345227669.4, 95959767.38, 2027421.375, -263510.3783, -3736.317347,
    -19320679.71, 53663186.78, 181453289.1, 125363205.3, -167139214.9
]

# Creating a DEA input/output table
data = pd.DataFrame({
    "Input": inputs,
    "CO2 Reduction": co2_reductions,
    "Employment": employment_impacts,
    "Value Added": value_added
})

# Save to CSV for pyDEA (pyDEA expects input from files)
data.to_csv('/mnt/data/dea_data.csv', index=False)

# Running DEA analysis (output-oriented, CRS)
dea_result = run_dea(
    input_data='/mnt/data/dea_data.csv',
    orientation='output',
    returns='CRS',
    efficiency_measure='both',
    output_file='/mnt/data/dea_output.csv'
)

# Reading and displaying results
efficiency_results = pd.read_csv('/mnt/data/dea_output.csv')
efficiency_results
