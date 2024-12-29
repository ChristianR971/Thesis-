# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:01:08 2024

@author: C-att
"""

#%% Importing MARIO 
import mario
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


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
path_aggr = 'Aggregations/aggregation_2.xlsx'
#data_exio.get_aggregation_excel(path = path_aggr,) # Use only when it's a new aggregation
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

#%% Define the indicators:
    
CO2_all = ['CO2 - combustion - air',
           'CO2 - non combustion - Cement production - air',
           'CO2 - non combustion - Lime production - air']

Employment = ['Employment: Low-skilled male', 
'Employment: Low-skilled female',
'Employment: Medium-skilled male',
'Employment: Medium-skilled female',
'Employment: High-skilled male',
'Employment: High-skilled female']

ValueAdded = ['Taxes less subsidies on products purchased: Total',
'Other net taxes on production',
"Compensation of employees; wages, salaries, & employers' social contributions: Low-skilled",
"Compensation of employees; wages, salaries, & employers' social contributions: Medium-skilled",
"Compensation of employees; wages, salaries, & employers' social contributions: High-skilled",
'Operating surplus: Consumption of fixed capital',
'Operating surplus: Rents on land',
'Operating surplus: Royalties on resources',
'Operating surplus: Remaining net operating surplus']



#%% Baseline Scenario 2011

CO2_baseline = data_exio.query(
    matrices='E',
    scenarios='baseline',
    ).loc[CO2_all].sum()

Emp_baseline1 = data_exio.query(
    matrices='E',
    scenarios='baseline',
    ).loc[Employment].sum()

VA_baseline = data_exio.query(
    matrices='V',
    scenarios='baseline',
    ).loc[(ValueAdded)].sum()

#%% Calculation Intervention 1, Steel :
    # Intervention: Modular Design could give a 10.5% decrease in manufacturing of basic iron and steel 

path_s1 = "Sensitivity_analysis/S_Intervention 2.1.xlsx" 
#data_exio.get_shock_excel(path=path_s1) 
#%%

data_exio.shock_calc(
    io= path_s1,
    z= True,
    scenario='S_Intervention 2.1',
    force_rewrite=True,
    notes=['S_Intervention 2.1'])

#%% CO2 shock calculations Intervention 1

CO2_s1 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.1',
    ).loc[CO2_all].sum()

delta_E_s1 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.1',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s1_EU = delta_E_s1.head(25)
delta_E_s1_RoW = delta_E_s1.tail(25)
#%% Employment shock calculations Intervention 1

Emp_1 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.1',
    ).loc[Employment].sum()

delta_Emp_1 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.1',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_1_EU = delta_Emp_1.head(25)
delta_Emp_1_RoW = delta_Emp_1.tail(25)

#%% Value Added shock calculations Intervention 1 

VA_s1 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.1',
    ).loc[ValueAdded].sum()

delta_VA_s1 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.1",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s1_EU = delta_VA_s1.head(25)
delta_VA_s1_RoW = delta_VA_s1.tail(25)

#%% Calculation Scenario 2: Scrap Diversion 
#%% Calculation Intervention 2, Steel :
    # Intervention:Scrap diversion could reduce 14% of the scrap in construction 
    # which is 35% of the steel market. Which is a decrease of 4,9%

path_s2 = "Sensitivity_analysis/S_Intervention 2.2.xlsx" 
#data_exio.get_shock_excel(path=path_s2) 

#%%
data_exio.shock_calc(
    io= path_s2,
    z= True,
    scenario='S_Intervention 2.2',
    force_rewrite=True,
    notes=['S_Intervention 2.2'
           ])

#%% CO2 shock calculations scenario 2
CO2_s2 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.2',
    ).loc[CO2_all].sum()

delta_E_s2 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.2',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s2_EU = delta_E_s2.head(25)
delta_E_s2_RoW = delta_E_s2.tail(25)
#%%
Emp_2 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.2',
    ).loc[Employment].sum()

delta_Emp_2 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.2',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_2_EU = delta_Emp_2.head(25)
delta_Emp_2_RoW = delta_Emp_2.tail(25)
#%%

VA_s2 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.2',
    ).loc[ValueAdded].sum()

delta_VA_s2 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.2",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s2_EU = delta_VA_s2.head(22)
delta_VA_s2_RoW = delta_VA_s2.tail(22)

#%% Scenario 3: Improvement of Yield scrap 
#%% Intervention: Reduction of scrap in the manufacturing process of steel. 
# Could decrease 26% of steel manufacturing, + MP. Decrease of 9,1% 
path_s3 = "Sensitivity_analysis/S_Intervention 2.3.xlsx" 
#data_exio.get_shock_excel(path=path_s3) 

#%%
data_exio.shock_calc(
    io= path_s3,
    z= True,
    scenario='S_Intervention 2.3',
    force_rewrite=True,
    notes=['S_Intervention 2.3'
           ])

#%%
CO2_s3 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.3',
    ).loc[CO2_all].sum()

delta_E_s3 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.3',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()



delta_E_s3_EU = delta_E_s3.head(25)
delta_E_s3_RoW = delta_E_s3.tail(25)

#%%
Emp_3 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.3',
    ).loc[Employment].sum()

delta_Emp_3 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.3',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_3_EU = delta_Emp_3.head(25)
delta_Emp_3_RoW = delta_Emp_3.tail(25)

#%%

VA_s3 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.3',
    ).loc[ValueAdded].sum()

delta_VA_s3 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.3",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s3_EU = delta_VA_s3.head(25)
delta_VA_s3_RoW = delta_VA_s3.tail(25)

#%% Intervention 4: Building with Steel weight optimization to Decrease 5% in Steel production 
path_s4 = "Sensitivity_analysis/S_Intervention 2.4.xlsx" 
#data_exio.get_shock_excel(path=path_s4) 

#%%
data_exio.shock_calc(
    io= path_s4,
    z= True,
    scenario='S_Intervention 2.4',
    force_rewrite=True,
    notes=['S_Intervention 2.4'
           ])

#%%
CO2_s4 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.4',
    ).loc[CO2_all].sum()

delta_E_s4 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.4',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s4_EU = delta_E_s4.head(25)
delta_E_s4_RoW = delta_E_s4.tail(25)

#%%
Emp_4 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.4',
    ).loc[Employment].sum()

delta_Emp_4 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.4',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_4_EU = delta_Emp_4.head(25)
delta_Emp_4_RoW = delta_Emp_4.tail(25)

#%%

VA_s4 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.4',
    ).loc[ValueAdded].sum()

delta_VA_s4 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.4",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s4_EU = delta_VA_s4.head(25)
delta_VA_s4_RoW = delta_VA_s4.tail(25)

#%% Scenario 5: Re-manufacturing rebar waste 
# Intervention is the remanufacturing of rebar waste. This intervention could
# increase 10,5 % of the steel recycling. 

path_s5 = "Sensitivity_analysis/S_Intervention 2.5.xlsx" 
#data_exio.get_shock_excel(path=path_s5) 
#%%
data_exio.shock_calc(
    io= path_s5,
    z= True,
    scenario='S_Intervention 2.5',
    force_rewrite=True,
    notes=['S_Intervention 2.5'
           ])
#%%
CO2_s5 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.5',
    ).loc[CO2_all].sum()

delta_E_s5 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.5',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s5_EU = delta_E_s5.head(25)
delta_E_s5_RoW = delta_E_s5.tail(25)
#%%
Emp_5 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.5',
    ).loc[Employment].sum()
delta_Emp_5 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.5',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_5_EU = delta_Emp_5.head(25)
delta_Emp_5_RoW = delta_Emp_5.tail(25)
#%%
VA_s5 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.5',
    ).loc[ValueAdded].sum()
delta_VA_s5 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.5",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s5_EU = delta_VA_s5.head(25)
delta_VA_s5_RoW = delta_VA_s5.tail(25)

#%% Scenario 6: 3D printing
# This intervention could potentially decrease 4,7% of the Steel production 
path_s6 = "Sensitivity_analysis/S_Intervention 2.6.xlsx" 
#data_exio.get_shock_excel(path=path_s6) 
#%%
data_exio.shock_calc(
    io= path_s6,
    z= True,
    scenario='S_Intervention 2.6',
    force_rewrite=True,
    notes=['S_Intervention 2.6'
           ])
#%%
CO2_s6 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.6',
    ).loc[CO2_all].sum()
delta_E_s6 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.6',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s6_EU = delta_E_s6.head(25)
delta_E_s6_RoW = delta_E_s6.tail(25)

#%%
Emp_6 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.6',
    ).loc[Employment].sum()
delta_Emp_6 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.6',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_6_EU = delta_Emp_6.head(25)
delta_Emp_6_RoW = delta_Emp_6.tail(25)
#%%
VA_s6 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.6',
    ).loc[ValueAdded].sum()
delta_VA_s6 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.6",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s6_EU = delta_VA_s6.head(25)
delta_VA_s6_RoW = delta_VA_s6.tail(25)

#%% Scenario 7: Plastic deformation manufacturing
# This intervention could potentially increase recycling of aluminium by 2,6%  

path_s7 = "Sensitivity_analysis/S_Intervention 2.7.xlsx" 
#data_exio.get_shock_excel(path=path_s7) 
#%%
data_exio.shock_calc(
    io= path_s7,
    z= True,
    scenario='S_Intervention 2.7',
    force_rewrite=True,
    notes=['S_Intervention 2.7'
           ])
#%%
CO2_s7 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.7',
    ).loc[CO2_all].sum()
delta_E_s7 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.7',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s7_EU = delta_E_s7.head(25)
delta_E_s7_RoW = delta_E_s7.tail(25)


#%%
Emp_7 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.7',
    ).loc[Employment].sum()
delta_Emp_7 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.7',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_7_EU = delta_Emp_7.head(25)
delta_Emp_7_RoW = delta_Emp_7.tail(25)
#%%
VA_s7 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.7',
    ).loc[ValueAdded].sum()
delta_VA_s7 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.7",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s7_EU = delta_VA_s7.head(25)
delta_VA_s7_RoW = delta_VA_s7.tail(25)

#%% Scenario 8: Pyrolysis to improve recycling efficiency for aluminium 
#%%
# This method could improve material efficiency by 0,7% of the total construction sector. 
# This could also decrease aluminium production with 0,7% 
path_s8 = "Sensitivity_analysis/S_Intervention 2.8.xlsx" 
#data_exio.get_shock_excel(path=path_s8) 
#%%
data_exio.shock_calc(
    io= path_s8,
    z= True,
    scenario='S_Intervention 2.8',
    force_rewrite=True,
    notes=['S_Intervention 2.8'
           ])
#%%
CO2_s8 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.8',
    ).loc[CO2_all].sum()
delta_E_s8 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.8',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s8_EU = delta_E_s8.head(25)
delta_E_s8_RoW = delta_E_s8.tail(25)
#%%
Emp_8 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.8',
    ).loc[Employment].sum()
delta_Emp_8 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.8',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_8_EU = delta_Emp_8.head(25)
delta_Emp_8_RoW = delta_Emp_8.tail(25)
#%%
VA_s8 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.8',
    ).loc[ValueAdded].sum()
delta_VA_s8 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.8",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s8_EU = delta_VA_s8.head(25)
delta_VA_s8_RoW = delta_VA_s8.tail(25)

#%% Scenario 9: Adopting Design for Disassembly 
#%%
# This scenario could potentially decrease aluminium production with 3,5% 

path_s9 = "Sensitivity_analysis/S_Intervention 2.9.xlsx" 
#data_exio.get_shock_excel(path=path_s9) 
#%%
data_exio.shock_calc(
    io= path_s9,
    z= True,
    scenario='S_Intervention 2.9',
    force_rewrite=True,
    notes=['S_Intervention 2.9'
           ])
#%%
CO2_s9 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.9',
    ).loc[CO2_all].sum()
delta_E_s9 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.9',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s9_EU = delta_E_s9.head(25)
delta_E_s9_RoW = delta_E_s9.tail(25)
#%%
Emp_9 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.9',
    ).loc[Employment].sum()
delta_Emp_9 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.9',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_9_EU = delta_Emp_9.head(25)
delta_Emp_9_RoW = delta_Emp_9.tail(25)
#%%
VA_s9 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.9',
    ).loc[ValueAdded].sum()
delta_VA_s9 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.9",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s9_EU = delta_VA_s9.head(25)
delta_VA_s9_RoW = delta_VA_s9.tail(25)


#%% Scenario 10: Small changes in Facade design
#%%
# This intervention could decrease the aluminium mass and therefore 
#production with 5,6% 

path_s10 = "Sensitivity_analysis/S_Intervention 2.10.xlsx" 
#data_exio.get_shock_excel(path=path_s10) 
#%%
data_exio.shock_calc(
    io= path_s10,
    z= True,
    scenario='S_Intervention 2.10',
    force_rewrite=True,
    notes=['S_Intervention 2.10'
           ])
#%%
CO2_s10 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.10',
    ).loc[CO2_all].sum()
delta_E_s10 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.10',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()


delta_E_s10_EU = delta_E_s10.head(25)
delta_E_s10_RoW = delta_E_s10.tail(25)
#%%
Emp_10 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.10',
    ).loc[Employment].sum()
delta_Emp_10 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.10',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_10_EU = delta_Emp_10.head(25)
delta_Emp_10_RoW = delta_Emp_10.tail(25)
#%%
VA_s10 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.10',
    ).loc[ValueAdded].sum()
delta_VA_s10 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.10",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s10_EU = delta_VA_s10.head(25)
delta_VA_s10_RoW = delta_VA_s10.tail(25)

#%% Scenario 11: Using Recycled Aggregates of conventional ingredients 
#%%
# This intervention could potentially decrease manufacturing cement production 
# with 0,1%. 
path_s11 = "Sensitivity_analysis/S_Intervention 2.11.xlsx" 
#data_exio.get_shock_excel(path=path_s11) 
#%%
data_exio.shock_calc(
    io= path_s11,
    z= True,
    scenario='S_Intervention 2.11',
    force_rewrite=True,
    notes=['S_Intervention 2.11'
           ])
#%%
CO2_s11 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.11',
    ).loc[CO2_all].sum()
delta_E_s11 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.11',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s11_EU = delta_E_s11.head(25)
delta_E_s11_RoW = delta_E_s11.tail(25)
#%%
Emp_11 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.11',
    ).loc[Employment].sum()
delta_Emp_11 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.11',
    base_scenario='baseline',
    type='absolute'
    ).loc[Employment].sum()

delta_Emp_11_EU = delta_Emp_11.head(25)
delta_Emp_11_RoW = delta_Emp_11.tail(25)
#%%
VA_s11 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.11',
    ).loc[ValueAdded].sum()
delta_VA_s11 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.11",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s11_EU = delta_VA_s11.head(25)
delta_VA_s11_RoW = delta_VA_s11.tail(25)

#%% Scenario 12: Using steel slag for cement properties
#%% 
# This intervention has a primary change of 4,3% of decrease in cement manufacturing
# and a secondary change of 4,3% increase in Steel recycling. 

path_s12 = "Sensitivity_analysis/S_Intervention 2.12.xlsx" 
#data_exio.get_shock_excel(path=path_s12) 
#%%
data_exio.shock_calc(
    io= path_s12,
    z= True,
    scenario='S_Intervention 2.12',
    force_rewrite=True,
    notes=['S_Intervention 2.12'
           ])
#%%
CO2_s12 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.12',
    ).loc[CO2_all].sum()
delta_E_s12 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.12',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s12_EU = delta_E_s12.head(25)
delta_E_s12_RoW = delta_E_s12.tail(25)
#%%
Emp_12 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.12',
    ).loc[Employment].sum()
delta_Emp_12 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.12',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_12_EU = delta_Emp_12.head(25)
delta_Emp_12_RoW = delta_Emp_12.tail(25)
#%%
VA_s12 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.12',
    ).loc[ValueAdded].sum()
delta_VA_s12 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.12",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s12_EU = delta_VA_s12.head(25)
delta_VA_s12_RoW = delta_VA_s12.tail(25)

#%% Scenario 13: Using 3D printing to optimize concrete constructions
#%%
# This intervention could potentially decrease Concrete use by 14,4% in in the total
# construction sector. 
path_s13 = "Sensitivity_analysis/S_Intervention 2.13.xlsx" 
#data_exio.get_shock_excel(path=path_s13) 
#%%
data_exio.shock_calc(
    io= path_s13,
    z= True,
    scenario='S_Intervention 2.13',
    force_rewrite=True,
    notes=['S_Intervention 2.13'
           ])
#%%
CO2_s13 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.13',
    ).loc[CO2_all].sum()
delta_E_s13 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.13',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s13_EU = delta_E_s13.head(25)
delta_E_s13_RoW = delta_E_s13.tail(25)
#%%
Emp_13 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.13',
    ).loc[Employment].sum()
delta_Emp_13 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.13',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_13_EU = delta_Emp_13.head(25)
delta_Emp_13_RoW = delta_Emp_13.tail(25)
#%%
VA_s13 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.13',
    ).loc[ValueAdded].sum()
delta_VA_s13 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.13",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s13_EU = delta_VA_s13.head(25)
delta_VA_s13_RoW = delta_VA_s13.tail(25)

#%% Scenario 14: Using sustainable concrete by incorperating Aluminium dross and iron slag
#%%
# This intervention could potentially decrease concrete use by 18% in the entire construction industry
# As a secondary change it increase Re-processing aluminium and Re-processing Steel by 5% and 20%
path_s14 = "Sensitivity_analysis/S_Intervention 2.14.xlsx" 
#data_exio.get_shock_excel(path=path_s14) 
#%%
data_exio.shock_calc(
    io= path_s14,
    z= True,
    scenario='S_Intervention 2.14',
    force_rewrite=True,
    notes=['S_Intervention 2.14'
           ])
#%%
CO2_s14 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.14',
    ).loc[CO2_all].sum()
delta_E_s14 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.14',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s14_EU = delta_E_s14.head(25)
delta_E_s14_RoW = delta_E_s14.tail(25)
#%%
Emp_14 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.14',
    ).loc[Employment].sum()
delta_Emp_14 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.14',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_14_EU = delta_Emp_14.head(25)
delta_Emp_14_RoW = delta_Emp_14.tail(25)
#%%
VA_s14 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.14',
    ).loc[ValueAdded].sum()
delta_VA_s14 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.14",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s14_EU = delta_VA_s14.head(25)
delta_VA_s14_RoW = delta_VA_s14.tail(25)

#%% Scenario 15: Using Fly ash as a recycled aggregate for cement 
#%%
# This intervention increases the Re-processing of Fly ash into clinker by 13,75%
# As secondary changes it could have a decrease in landfill of waste by 19,1% and 
# decrease Concrete manufacturing by 13,75%.  

path_s15 = "Sensitivity_analysis/S_Intervention 2.15.xlsx" 
#data_exio.get_shock_excel(path=path_s15) 
#%%
data_exio.shock_calc(
    io= path_s15,
    z= True,
    scenario='S_Intervention 2.15',
    force_rewrite=True,
    notes=['S_Intervention 2.15'
           ])
#%%
CO2_s15 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.15',
    ).loc[CO2_all].sum()
delta_E_s15 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.15',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s15_EU = delta_E_s15.head(25)
delta_E_s15_RoW = delta_E_s15.tail(25)
#%%
Emp_15 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.15',
    ).loc[Employment].sum()
delta_Emp_15 = data_exio.query(
    matrices='E',
    scenarios='S_Intervention 2.15',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_15_EU = delta_Emp_15.head(25)
delta_Emp_15_RoW = delta_Emp_15.tail(25)
#%%
VA_s15 = data_exio.query(
    matrices='V',
    scenarios='S_Intervention 2.15',
    ).loc[ValueAdded].sum()
delta_VA_s15 = data_exio.query(
    matrices="V",
    scenarios="S_Intervention 2.15",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()
delta_VA_s15_EU = delta_VA_s15.head(25)
delta_VA_s15_RoW = delta_VA_s15.tail(25)

#%% Totals of CO2 emissions

delta_E_s1_total = delta_E_s1.sum()
delta_E_s2_total = delta_E_s2.sum()
delta_E_s3_total = delta_E_s3.sum()
delta_E_s4_total = delta_E_s4.sum()
delta_E_s5_total = delta_E_s5.sum()
delta_E_s6_total = delta_E_s6.sum()
delta_E_s7_total = delta_E_s7.sum()
delta_E_s8_total = delta_E_s8.sum()
delta_E_s9_total = delta_E_s9.sum()
delta_E_s10_total = delta_E_s10.sum()
delta_E_s11_total = delta_E_s11.sum()
delta_E_s12_total = delta_E_s12.sum()
delta_E_s13_total = delta_E_s13.sum()
delta_E_s14_total = delta_E_s14.sum()
delta_E_s15_total = delta_E_s15.sum()

delta_E_totals = pd.Series({
    'S1': delta_E_s1_total,
    'S2': delta_E_s2_total,
    'S3': delta_E_s3_total,
    'S4': delta_E_s4_total,
    'S5': delta_E_s5_total,
    'S6': delta_E_s6_total,
    'S7': delta_E_s7_total,
    'S8': delta_E_s8_total,
    'S9': delta_E_s9_total,
    'S10': delta_E_s10_total,
    'S11': delta_E_s11_total,
    'S12': delta_E_s12_total,
    'S13': delta_E_s13_total,
    'S14': delta_E_s14_total,
    'S15': delta_E_s15_total
})

#%%
delta_E_all_totals = delta_E_totals.sum()

#%%
# Create a list of all delta_E variables
deltas_E = [delta_E_s1, delta_E_s2, delta_E_s3, delta_E_s4, delta_E_s5, 
          delta_E_s6, delta_E_s7, delta_E_s8, delta_E_s9, delta_E_s10,
          delta_E_s11, delta_E_s12, delta_E_s13, delta_E_s14, delta_E_s15]

# Create a DataFrame with all scenarios
df_combined = pd.concat(deltas_E, axis=1)
df_combined.columns = [f'S{i+1}' for i in range(15)]

# Find the minimum value (maximum reduction) for each sector across all scenarios
min_values = df_combined.min(axis=1)
max_reduction = min_values.min()
sector_with_max_reduction = min_values.idxmin()
scenario_with_max_reduction = df_combined.loc[sector_with_max_reduction].idxmin()

# Print results
print(f"Sector with maximum CO2 reduction: {sector_with_max_reduction}")
print(f"Maximum reduction value: {max_reduction:.2e}")
print(f"This occurred in scenario: {scenario_with_max_reduction}")

# Show top 5 sectors with highest reductions
print("\nTop 5 sectors with highest reductions:")
top_5_reductions = min_values.sort_values().head()
for sector, value in top_5_reductions.items():
    print(f"{sector}: {value:.2e}")

# Create a dictionary showing which scenario achieved the maximum reduction for each sector
max_reduction_scenarios = {}
for sector in df_combined.index:
    scenario = df_combined.loc[sector].idxmin()
    value = df_combined.loc[sector, scenario]
    max_reduction_scenarios[sector] = (scenario, value)

print("\nBest performing scenario for each sector:")
for sector, (scenario, value) in max_reduction_scenarios.items():
    print(f"{sector}: {scenario} (reduction: {value:.2e})")
    

#%% Totals of Employment
delta_Emp_1_total = delta_Emp_1.sum()  
delta_Emp_2_total = delta_Emp_2.sum()  
delta_Emp_3_total = delta_Emp_3.sum() 
delta_Emp_4_total = delta_Emp_4.sum() 
delta_Emp_5_total = delta_Emp_5.sum()  
delta_Emp_6_total = delta_Emp_6.sum()  
delta_Emp_7_total = delta_Emp_7.sum()  
delta_Emp_8_total = delta_Emp_8.sum()  
delta_Emp_9_total = delta_Emp_9.sum() 
delta_Emp_10_total = delta_Emp_10.sum()  
delta_Emp_11_total = delta_Emp_11.sum()  
delta_Emp_12_total = delta_Emp_12.sum() 
delta_Emp_13_total = delta_Emp_13.sum()  
delta_Emp_14_total = delta_Emp_14.sum()  
delta_Emp_15_total = delta_Emp_15.sum() 

delta_Emp_totals = pd.Series({
    'S1': delta_Emp_1_total,
    'S2': delta_Emp_2_total,
    'S3': delta_Emp_3_total,
    'S4': delta_Emp_4_total,
    'S5': delta_Emp_5_total,
    'S6': delta_Emp_6_total,
    'S7': delta_Emp_7_total,
    'S8': delta_Emp_8_total,
    'S9': delta_Emp_9_total,
    'S10': delta_Emp_10_total,
    'S11': delta_Emp_11_total,
    'S12': delta_Emp_12_total,
    'S13': delta_Emp_13_total,
    'S14': delta_Emp_14_total,
    'S15': delta_Emp_15_total
})


#%% Totals of Value Added

# Summing delta_VA for VA
delta_VA_1_total = delta_VA_s1.sum()
delta_VA_2_total = delta_VA_s2.sum()
delta_VA_3_total = delta_VA_s3.sum()
delta_VA_4_total = delta_VA_s4.sum()
delta_VA_5_total = delta_VA_s5.sum()
delta_VA_6_total = delta_VA_s6.sum()
delta_VA_7_total = delta_VA_s7.sum()
delta_VA_8_total = delta_VA_s8.sum()
delta_VA_9_total = delta_VA_s9.sum()
delta_VA_10_total = delta_VA_s10.sum()
delta_VA_11_total = delta_VA_s11.sum()
delta_VA_12_total = delta_VA_s12.sum()
delta_VA_13_total = delta_VA_s13.sum()
delta_VA_14_total = delta_VA_s14.sum()
delta_VA_15_total = delta_VA_s15.sum()

# Creating a Series for all delta_VA totals
delta_VA_totals = pd.Series({
    'S1': delta_VA_1_total,
    'S2': delta_VA_2_total,
    'S3': delta_VA_3_total,
    'S4': delta_VA_4_total,
    'S5': delta_VA_5_total,
    'S6': delta_VA_6_total,
    'S7': delta_VA_7_total,
    'S8': delta_VA_8_total,
    'S9': delta_VA_9_total,
    'S10': delta_VA_10_total,
    'S11': delta_VA_11_total,
    'S12': delta_VA_12_total,
    'S13': delta_VA_13_total,
    'S14': delta_VA_14_total,
    'S15': delta_VA_15_total
})

#%%

# Create DataFrame
data = {
    'Delta_Emissions': delta_E_totals,
    'Delta_Employment': delta_Emp_totals,
    'Delta_Value_Added': delta_VA_totals
}

df = pd.DataFrame(data)

# Add intervention numbers
df.index = [f'Intervention {i+1}' for i in range(len(df))]

# Export to Excel
df.to_excel('Sensitivity 5%_results.xlsx')
print("Data exported to 'intervention_results.xlsx'")


#%%

emissions_5 = [-1.7E+08, -7.2E+07, -5.7E+08, -3.1E+08, -4.5E+07, -4.9E+08, -7562338, 
               -2337377, -3448642, -1.4E+07, -1.8E+08, 37608273, -3.3E+08, -1.9E+07, -4.1E+08]

emissions_2 = [-1.4E+08, -5E+07, -4.5E+08, -2.2E+08, -2.4E+07, -3.4E+08, -3575165, 
               -1124206, -2235471, -1E+07, -9.1E+07, 25502605, -3.1E+08, -3.4E+07, -3.4E+08]

emissions_0 = [-117423057.3, -35516080.36, -379481916, -261504734.9, -7610589.044,
               -239377416.2, -3455549.736, -294396.2818, -1426689.687, -7442722.482,
               -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5]

plt.figure(figsize=(12, 10))
y = np.arange(len(emissions_5))
width = 0.25

plt.barh(y - width, emissions_5, width, label='5% Sensitivity', color='darkred', alpha=0.7)
plt.barh(y, emissions_2, width, label='2% Sensitivity', color='lightcoral', alpha=0.7)
plt.barh(y + width, emissions_0, width, label='Counterfactual', color='indianred', alpha=0.7)

plt.title('Delta Emissions: Sensitivity Analysis Comparison')
plt.xlabel('Delta Emissions from Baseline')
plt.ylabel('Intervention Number')
plt.yticks(y, [f'Int {i+1}' for i in range(len(emissions_5))])
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.legend()

plt.tight_layout()
plt.savefig('emissions_comparison_horizontal.png', dpi=100)
plt.show()



#%%
# Data setup
emissions_5 = [-173338802.2, -71756973.84, -566736518.9, -312864638.2, -45301122.08,
               -490824164.7, -10100837.64, -2316348.787, -3448642.191, -14088010.34,
               -180198757.6, 37608273.48, -326028667.2, -18876608.71, -405728941.7]

emissions_2 = [-139789355, -50012438.34, -445293014.8, -220845630.6, -9060225.025,
               -339956130, -6113664.903, -1103177.286, -2235470.689, -10100837.64,
               -37936581.66, 25502605.47, -310557835.5, -33756277.71, -340812315.4]

# Create plot
plt.figure(figsize=(15, 10))
x = np.arange(len(emissions_5))
width = 0.35

plt.bar(x - width/2, emissions_5, width, label='5% Sensitivity', color='darkred', alpha=0.7)
plt.bar(x + width/2, emissions_2, width, label='2% Sensitivity', color='lightcoral', alpha=0.7)

plt.title('Delta Emissions: 5% vs 2% Sensitivity Analysis')
plt.xlabel('Intervention Number')
plt.ylabel('Delta Emissions')
plt.xticks(x, [f'Int {i+1}' for i in range(len(emissions_5))])
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.legend()

plt.tight_layout()
plt.savefig('emissions_comparison.png', dpi=100)
plt.show()

#%%


emissions_5 = [-173338802.2, -71756973.84, -566736518.9, -312864638.2, -45301122.08,
               -490824164.7, -10100837.64, -2316348.787, -3448642.191, -14088010.34,
               -180198757.6, 37608273.48, -326028667.2, -18876608.71, -405728941.7]

emissions_2 = [-139789355, -50012438.34, -445293014.8, -220845630.6, -9060225.025,
               -339956130, -6113664.903, -1103177.286, -2235470.689, -10100837.64,
               -37936581.66, 25502605.47, -310557835.5, -33756277.71, -340812315.4]

emissions_0 = [-117423057.3, -35516080.36, -379481916, -261504734.9, -7610589.044,
               -239377416.2, -3455549.736, -294396.2818, -1426689.687, -7442722.482,
               -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5]

plt.figure(figsize=(12, 10))
y = np.arange(len(emissions_5))
width = 0.25

plt.barh(y - width, emissions_5, width, label='5% Sensitivity', color='darkredw', alpha=0.7)
plt.barh(y, emissions_2, width, label='2% Sensitivity', color='lightcoral', alpha=0.7)
plt.barh(y + width, emissions_0, width, label='Baseline', color='indianred', alpha=0.7)

plt.title('Delta Emissions: Sensitivity Analysis Comparison')
plt.xlabel('Delta Emissions from Baseline')
plt.ylabel('Intervention Number')
plt.yticks(y, [f'Int {i+1}' for i in range(len(emissions_5))])
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.legend()

plt.tight_layout()
plt.savefig('emissions_comparison_horizontal.png', dpi=100)
plt.show()

#%%

# Calculate totals
emissions_5_totals = sum(emissions_5)
emissions_2_totals = sum(emissions_2)
emissions_0_totals = sum(emissions_0)

# Create plot
plt.figure(figsize=(10, 6))

x = np.arange(3)
totals = [emissions_5_totals, emissions_2_totals, emissions_0_totals]
labels = ['5% Sensitivity', '2% Sensitivity', 'Counterfactual']
colors = ['darkred', 'lightcoral', 'indianred']

bars = plt.bar(x, totals, color=colors, alpha=0.7)

plt.title('Total Delta Emissions Across All Interventions')
plt.ylabel('Total Delta Emissions')
plt.xticks(x, labels)
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('total_emissions_comparison.png', dpi=100)
plt.show()

#%%



# Data for the datasets
delta_employment_2 = [
    10.8508183, -2.528562781, -10.70507568, -2.121789254, -1.190989774,
    -11.1791258, -0.108274908, -0.004124058, -0.008200646, -0.3059068,
    -1.110887636, 1.732676112, 5.963453707, 3.51601986, -3.907984833
]

delta_employment_5 = [
    13.45501485, -3.627937756, -13.62464068, -2.999770965, -2.290364857,
    -16.14027399, -0.229027592, -0.008574482, -0.012651069, -0.426659483,
    -2.192921007, 2.555149007, 9.859014447, 4.454795137, -4.652362838
]

counterfactual = [
    9.114687303, -1.795646081, -8.75869875, -8.103213209, -3.847812739,
    -7.871692884, 1.85265913, 0.02911293, -0.005233698, -0.225405011,
    -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282
]

# Interventions
interventions = np.arange(1, 16)

# Creating the bar chart with specified order: 5%, 2%, Counterfactual
bar_width = 0.25
y_positions = np.arange(len(interventions))

plt.figure(figsize=(12, 8))

plt.barh(y_positions - bar_width, delta_employment_5, height=bar_width, label="Delta Employment 5%", color='navy', alpha=0.7)
plt.barh(y_positions, delta_employment_2, height=bar_width, label="Delta Employment 2%", color='blue', alpha=0.7)
plt.barh(y_positions + bar_width, counterfactual, height=bar_width, label="Counterfactual", color='lightblue', alpha=0.7)

# Adding labels, title, and legend
plt.xlabel("Employment Impact Value (1000 p)", fontsize=12)
plt.ylabel("Interventions", fontsize=12)
plt.yticks(y_positions, [f"Intervention {i}" for i in interventions])
plt.axvline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.7)
plt.title("Sensitivity analysis of Employment Impact Across Interventions ", fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.4, axis='x')

# Display the chart
plt.tight_layout()
plt.show()

#%%


# Data
va_5 = [652.1843, -140.751, -601.204, -136.935, -88.8578, -707.862, -8.612, 
        -0.43171, -0.63697, -16.0435, -108.768, 115.7734, 516.163, 194.6676, -227.917]

va_2 = [525.9551, -98.099, -472.375, -96.8561, -46.2061, -490.281, -4.0714,
        -0.20764, -0.41289, -11.5029, -55.0997, 78.50726, 315.3372, 153.085, -191.45]

va_0 = [441.8022859, -69.66453618, -386.48829, -355.381422, -149.2811376, -345.2276694,
        95.95976738, 2.027421375, -0.263510378, -0.003736317, -19.32067971, 53.66318678,
        181.4532891, 125.3632053, -167.1392149]

# Calculate totals
va_5_total = sum(va_5)
va_2_total = sum(va_2)
va_0_total = sum(va_0)

# Create plot
plt.figure(figsize=(10, 6))

x = np.arange(3)
totals = [va_5_total, va_2_total, va_0_total]
labels = ['5% Sensitivity', '2% Sensitivity', 'Baseline']
colors = ['darkgreen', 'lightgreen', 'forestgreen']

bars = plt.bar(x, totals, color=colors, alpha=0.7)

plt.title('Total Delta Value Added Across All Interventions')
plt.ylabel('Total Delta Value Added (M€)')
plt.xticks(x, labels)
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.1f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('total_value_added_comparison.png', dpi=100)
plt.show()

#%%

# Data
va_5 = [652.1843, -140.751, -601.204, -136.935, -88.8578, -707.862, -8.612, 
        -0.43171, -0.63697, -16.0435, -108.768, 115.7734, 516.163, 194.6676, -227.917]

va_2 = [525.9551, -98.099, -472.375, -96.8561, -46.2061, -490.281, -4.0714,
        -0.20764, -0.41289, -11.5029, -55.0997, 78.50726, 315.3372, 153.085, -191.45]

va_0 = [441.8022859, -69.66453618, -386.48829, -355.381422, -149.2811376, -345.2276694,
        95.95976738, 2.027421375, -0.263510378, -0.003736317, -19.32067971, 53.66318678,
        181.4532891, 125.3632053, -167.1392149]

plt.figure(figsize=(12, 10))
y = np.arange(len(va_5))
width = 0.25

plt.barh(y - width, va_5, width, label='5% Sensitivity', color='darkgreen', alpha=0.7)
plt.barh(y, va_2, width, label='2% Sensitivity', color='forestgreen', alpha=0.7)
plt.barh(y + width, va_0, width, label='Counterfactual', color='lightgreen', alpha=0.7)

plt.title('Delta Value Added: Sensitivity Analysis Comparison')
plt.xlabel('Delta Value Added (M€)')
plt.ylabel('Intervention Number')
plt.yticks(y, [f'Int {i+1}' for i in range(len(va_5))])
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.legend()

plt.tight_layout()
plt.savefig('value_added_comparison_horizontal.png', dpi=100)
plt.show()