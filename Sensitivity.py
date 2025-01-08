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

# Convert scientific notation with commas to standard format
emissions_5 = [-1.7e8, -7.2e7, -5.7e8, -5.2e8, -4.4e7, -4.9e8, -7564996, -2316349, -3448642, -1.4e7, -1.8e8, 37608273, -3.3e8, -5.5e7, -4.1e8]
emissions_2 = [-1.4E+08, -5E+07, -4.5E+08, -3.6E+08, -2.2E+07, -3.4E+08, -3577823, -1103177, -2235471, -1E+07, -9.1E+07, 25502605, -3.1E+08, -3.5E+07, -3.4E+08]
emissions_05 = [-1.2E+08, -3.9E+07, -3.9E+08, -2.9E+08, -7972998, -2.6E+08, -1584237, -496592, -1628885, -8107251, -4.7E+07, 19449772, -3E+08, -4.1E+07, -3.1E+08]
emissions_0 = [-117423057.3, -35516080.36, -379481916, -261504734.9, -7610589.044, -239377416.2, -919707.8518, -294396.2818, -1426689.687, -7442722.482, -32008990.82, 17432160.44, -300243948.9, -43676056.62, -297534563.5]

plt.figure(figsize=(15, 12))
y = np.arange(len(emissions_5))
width = 0.2

plt.barh(y - width*1.5, emissions_5, width, label='5% Sensitivity', color='darkred', alpha=0.7)
plt.barh(y - width*0.5, emissions_2, width, label='2% Sensitivity', color='lightcoral', alpha=0.7)
plt.barh(y + width*0.5, emissions_05, width, label='0.5% Sensitivity', color='indianred', alpha=0.7)
plt.barh(y + width*1.5, emissions_0, width, label='Counterfactual', color='rosybrown', alpha=0.7)

def format_ticks(x, _):
    return f'{x/1e6:,.0f}M'

plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_ticks))

plt.title('Delta Emissions: Sensitivity Analysis Comparison', fontsize=14, pad=20)
plt.xlabel('Delta Emissions from Baseline (Millions)', fontsize=12)
plt.ylabel('Intervention Number', fontsize=12)
plt.yticks(y, [f'Int {i+1}' for i in range(len(emissions_5))], fontsize=10)

plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)
plt.tight_layout()

plt.savefig('emissions_comparison_horizontal.png', dpi=300, bbox_inches='tight')
plt.show()


#%%
# Calculate totals 
emissions_5_totals = sum(emissions_5)
emissions_2_totals = sum(emissions_2)
emissions_05_totals = sum(emissions_05)
emissions_0_totals = sum(emissions_0)

# Create plot
plt.figure(figsize=(10, 6))
x = np.arange(4)  # Changed to 4 to accommodate the new level
totals = [emissions_5_totals, emissions_2_totals, emissions_05_totals, emissions_0_totals]
labels = ['5% Sensitivity', '2% Sensitivity', '0.5% Sensitivity', 'Counterfactual']
colors = ['darkred', 'red', 'lightcoral', 'indianred']

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

emp_5 = [13.45501, -3.62794, -13.722, -16.9506, -2.21707, -16.1403, -0.22911, -0.0085, -0.01265, -0.42666, -2.19292, 2.555149, 9.859014, 3.731762, -4.65236]
emp_2 = [10.85082, -2.52856, -10.8024, -11.9894, -1.1177, -11.1791, -0.10836, -0.00405, -0.0082, -0.30591, -1.11089, 1.732676, 5.963454, 3.477252, -3.90798]
emp_05 = [9.54872, -1.97888, -9.34261, -9.50887, -0.4031, -8.69855, -0.04798, -0.00182, -0.00598, -0.24553, -0.56987, 1.32144, 4.015674, 3.046632, -3.53629]
emp_0 = [9.114687303, -1.795646081, -8.75869875, -8.103213209, -3.847812739, -7.871692884, -0.02785362, 0.02911293, -0.005233698, -0.225405011, -0.389532033, 1.184360868, 3.36641353, 2.890169701, -3.41173282]

plt.figure(figsize=(15, 12))
y = np.arange(len(emp_5))
width = 0.2

plt.barh(y - width*1.5, emp_5, width, label='5% Sensitivity', color='darkblue', alpha=0.7)
plt.barh(y - width*0.5, emp_2, width, label='2% Sensitivity', color='royalblue', alpha=0.7)
plt.barh(y + width*0.5, emp_05, width, label='0.5% Sensitivity', color='cornflowerblue', alpha=0.7)
plt.barh(y + width*1.5, emp_0, width, label='Counterfactual', color='lightsteelblue', alpha=0.7)

plt.title('Delta Employment: Sensitivity Analysis Comparison', fontsize=14, pad=20)
plt.xlabel('Delta Employment (FTE)', fontsize=12)
plt.ylabel('Intervention Number', fontsize=12)
plt.yticks(y, [f'Int {i+1}' for i in range(len(emp_5))], fontsize=10)

plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)
plt.tight_layout()

plt.savefig('employment_comparison_horizontal.png', dpi=300, bbox_inches='tight')
plt.show()

#%%


# Calculate totals for employment
employment_5_totals = sum(emp_5)
employment_2_totals = sum(emp_2)
employment_05_totals = sum(emp_05)
employment_0_totals = sum(emp_0)

# Create plot
plt.figure(figsize=(10, 6))
x = np.arange(4)
totals = [employment_5_totals, employment_2_totals, employment_05_totals, employment_0_totals]
labels = ['5% Sensitivity', '2% Sensitivity', '0.5% Sensitivity', 'Counterfactual']
colors = ['darkblue', 'blue', 'cornflowerblue', 'lightsteelblue']

bars = plt.bar(x, totals, color=colors, alpha=0.7)
plt.title('Total Delta Employment Across All Interventions')
plt.ylabel('Total Delta Employment (FTE)')
plt.xticks(x, labels)
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.0f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('total_employment_comparison.png', dpi=100)
plt.show()
#%%


#%%

# Data
va_0 = [441.8023, -69.6645, -386.488, -377.139, -14.9281, -345.228, 
        -1.04736, -0.05438, -0.26351, -8.47579, -19.3207, 53.66319, 
        181.4533, 125.3632, -167.139]
va_05 = [462.8405, -76.7732, -412.254, -417.029, -15.639, -381.491, 
         -1.80413, -0.09172, -0.30086, -9.23255, -28.2654, 59.8742, 
         214.9243, 132.2936, -173.241]
va_2 = [525.9551, -98.099, -476.669, -525.819, -43.3626, -490.281, 
        -4.07443, -0.20376, -0.41289, -11.5029, -55.0997, 78.50726, 
        315.3372, 151.6461, -191.45]
va_5 = [652.1843, -140.751, -605.498, -743.4, -86.0144, -707.862, 
        -8.61503, -0.42783, -0.63697, -16.0435, -108.768, 115.7734, 
        516.163, 161.6252, -227.917]

# First plot: Horizontal bar chart
plt.figure(figsize=(15, 10))
y = np.arange(len(va_0))
width = 0.2

# Plot bars
plt.barh(y - width*1.5, va_0, width, label='Baseline', color='#ffd700', alpha=0.8)
plt.barh(y - width/2, va_05, width, label='0.5% Sensitivity', color='#ffc400', alpha=0.8)
plt.barh(y + width/2, va_2, width, label='2% Sensitivity', color='#ffb300', alpha=0.8)
plt.barh(y + width*1.5, va_5, width, label='5% Sensitivity', color='#ffa000', alpha=0.8)

# Customize plot
plt.title('Delta Value Added: Sensitivity Analysis by Intervention', pad=20, fontsize=18, fontweight='bold')
plt.xlabel('Delta Value Added (M€)', fontsize=14)
plt.ylabel('Interventions', fontsize=14)
plt.yticks(y, [f'Int {i+1}' for i in range(len(va_0))])
plt.grid(True, linestyle='--', alpha=0.3, axis='x')
plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=4)

plt.tight_layout()
plt.savefig('value_added_comparison_horizontal.png', dpi=300, bbox_inches='tight')
plt.show()

# Second plot: Total values
plt.figure(figsize=(10, 6))
x = np.arange(4)

# Calculate totals
totals = [sum(va_5), sum(va_2), sum(va_05), sum(va_0)]
labels = ['5% Sensitivity', '2% Sensitivity', '0.5% Sensitivity', 'Baseline']
colors = ['#ffa000', '#ffb300', '#ffc400', '#ffd700']

# Create bars
bars = plt.bar(x, totals, color=colors, alpha=0.8)

# Customize plot
plt.title('Total Delta Value Added Across All Interventions', fontsize=14, fontweight='bold')
plt.ylabel('Total Delta Value Added (M€)')
plt.xticks(x, labels, rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.3, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:,.1f}',
             ha='center', va='bottom')

plt.tight_layout()
plt.savefig('total_value_added_comparison.png', dpi=300)
plt.show()