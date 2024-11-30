# Intervention-1
Code Thesis Intervention 1

#%% Importing MARIO 
import mario
import pandas as pd
import numpy as np


#%% Uploading Exiobase
IOT_path = 'IOT_2011_ixi'  # Define the desired path to the folder where Exiobase should be downloaded
data_exio = mario.parse_exiobase(
    table = 'IOT',
    unit = 'Monetary',
    path = IOT_path,)

#%% Test balance
data_exio.is_balanced('flows', data_set='baseline', margin=0.05, as_dataframe=False)

#%% Aggregating the data 

# Aggregation
path_aggr = 'Aggregations/aggregation_data.xlsx'
data_exio.get_aggregation_excel(path = path_aggr,) # Use only when it's a new aggregation
#%%
data_exio.aggregate(
    io=path_aggr,
    ignore_nan=True,
    levels = [
        "Consumption category",
        "Region",
        "Sector",])

#%%
data_exio.aggregate
#%% Exporting table
path_table = 'Aggregations/Table_IOT.xlsx'
data_exio.to_excel(
    path=path_table,
    flows=True,
    coefficients=True,)

#%% Calculation Intervention 1, Steel :
    # Intervention: Modular Design could give a 10.5% decrease in manufacturing of basic iron and steel 

path_s1 = "Scenarios/Intervention1.xlsx" 
data_exio.get_shock_excel(path=path_s1) 
#%%

data_exio.shock_calc(
    io= path_s1,
    Y= True,
    scenario='Intervention 1',
    force_rewrite=True,
    notes=['Reducing'])

#%% CO2 shock calculations Intervention 1

CO2_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    ).loc['CO2 - combustion - air'].sum()

CO2_baseline = data_exio.query(
    matrices='E',
    scenarios='baseline',
    ).loc['CO2 - combustion - air'].sum()

delta_E_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']

#%% Employment shock calculations Intervention 1

# Emp_s1 = data_exio.query(
#     matrices='E',
#     scenarios='Intervention 1',
#     ).loc[data_exio.index.isin([
#         'Employment: Low-skilled male', 
#         'Employment: Low-skilled female', 
#         'Employment: Medium-skilled male',
#         'Employment: Medium-skilled female',
#         'Employment: High-skilled male',
#         'Employment: High-skilled female'
#     ])]

Emp_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    ).iloc[([
        'Employment: Low-skilled male', 
        'Employment: Low-skilled female',
        'Employment: Medium-skilled male',
        'Employment: Medium-skilled female',
        'Employment: High-skilled male',
        'Employment: High-skilled female'
        ])]

