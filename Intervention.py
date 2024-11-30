# Intervention-1
Code Thesis Intervention 1

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

Employment = ['Employment: Low-skilled male', 
'Employment: Low-skilled female',
'Employment: Medium-skilled male',
'Employment: Medium-skilled female',
'Employment: High-skilled male',
'Employment: High-skilled female']


Emp_1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    ).loc[Employment].sum()


Emp_baseline1 = data_exio.query(
    matrices='E',
    scenarios='baseline',
    ).loc[Employment].sum()

delta_Emp_1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()

#%%

Emp_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    ).loc[([
        'Employment: Low-skilled male', 
        'Employment: Low-skilled female',
        'Employment: Medium-skilled male',
        'Employment: Medium-skilled female',
        'Employment: High-skilled male',
        'Employment: High-skilled female'
        ])].sum()

Emp_baseline = data_exio.query(
    matrices='E',
    scenarios='baseline',
    ).loc[([
        'Employment: Low-skilled male', 
        'Employment: Low-skilled female',
        'Employment: Medium-skilled male',
        'Employment: Medium-skilled female',
        'Employment: High-skilled male',
        'Employment: High-skilled female'
        ])].sum()

delta_Emp_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 1',
    base_scenario='baseline',
    type='relative',
    ).loc[([
        'Employment: Low-skilled male', 
        'Employment: Low-skilled female',
        'Employment: Medium-skilled male',
        'Employment: Medium-skilled female',
        'Employment: High-skilled male',
        'Employment: High-skilled female'
        ])].sum()
        
        
#%% Value Added shock calculations Intervention 1 
ValueAdded = ['Taxes less subsidies on products purchased: Total',
'Other net taxes on production',
'Compensation of employees; wages, salaries, & employers''social contributions: Low-skilled',
'Compensation of employees; wages, salaries, & employers' 'social contributions: Medium-skilled',
'Compensation of employees; wages, salaries, & employers' 'social contributions: High-skilled',
'Operating surplus: Consumption of fixed capital',
'Operating surplus: Rents on land',
'Operating surplus: Royalties on resources',
'Operating surplus: Remaining net operating surplus']

VA_s1 = data_exio.query(
    matrices='M',
    scenarios='Intervention 1',
    ).loc[ValueAdded].sum()

VA_baseline = data_exio.query(
    matrices='M',
    scenarios='baseline',
    ).loc[(ValueAdded)].sum()

delta_VA_s1 = data_exio.query(
    matrices="M",
    scenarios="Intervention 1",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()
