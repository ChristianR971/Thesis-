# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:45:08 2024

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

path_s1 = "Scenarios_2/Intervention 2.1.xlsx" 
#data_exio.get_shock_excel(path=path_s1) 
#%%

data_exio.shock_calc(
    io= path_s1,
    z= True,
    scenario='Intervention 2.1',
    force_rewrite=True,
    notes=['Intervention 2.1'])

#%% CO2 shock calculations Intervention 1

CO2_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.1',
    ).loc[CO2_all].sum()

delta_E_s1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.1',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s1_EU = delta_E_s1.head(25)
delta_E_s1_RoW = delta_E_s1.tail(25)
#%% Employment shock calculations Intervention 1

Emp_1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.1',
    ).loc[Employment].sum()

delta_Emp_1 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.1',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_1_EU = delta_Emp_1.head(25)
delta_Emp_1_RoW = delta_Emp_1.tail(25)

#%% Value Added shock calculations Intervention 1 

VA_s1 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.1',
    ).loc[ValueAdded].sum()

delta_VA_s1 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.1",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s1_EU = delta_VA_s1.head(25)
delta_VA_s1_RoW = delta_VA_s1.tail(25)

#%% Calculation Scenario 2: Scrap Diversion 
#%% Calculation Intervention 2, Steel :
    # Intervention:Scrap diversion could reduce 14% of the scrap in construction 
    # which is 35% of the steel market. Which is a decrease of 4,9%

path_s2 = "Scenarios_2/Intervention 2.2.xlsx" 
#data_exio.get_shock_excel(path=path_s2) 

#%%
data_exio.shock_calc(
    io= path_s2,
    z= True,
    scenario='Intervention 2.2',
    force_rewrite=True,
    notes=['Intervention 2.2'
           ])

#%% CO2 shock calculations scenario 2
CO2_s2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.2',
    ).loc[CO2_all].sum()

delta_E_s2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.2',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s2_EU = delta_E_s2.head(25)
delta_E_s2_RoW = delta_E_s2.tail(25)
#%%
Emp_2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.2',
    ).loc[Employment].sum()

delta_Emp_2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.2',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_2_EU = delta_Emp_2.head(25)
delta_Emp_2_RoW = delta_Emp_2.tail(25)
#%%

VA_s2 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.2',
    ).loc[ValueAdded].sum()

delta_VA_s2 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.2",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s2_EU = delta_VA_s2.head(22)
delta_VA_s2_RoW = delta_VA_s2.tail(22)

#%% Scenario 3: Improvement of Yield scrap 
#%% Intervention: Reduction of scrap in the manufacturing process of steel. 
# Could decrease 26% of steel manufacturing, + MP. Decrease of 9,1% 
path_s3 = "Scenarios_2/Intervention 2.3.xlsx" 
#data_exio.get_shock_excel(path=path_s3) 

#%%
data_exio.shock_calc(
    io= path_s3,
    z= True,
    scenario='Intervention 2.3',
    force_rewrite=True,
    notes=['Intervention 2.3'
           ])

#%%
CO2_s3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.3',
    ).loc[CO2_all].sum()

delta_E_s3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.3',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()



delta_E_s3_EU = delta_E_s3.head(25)
delta_E_s3_RoW = delta_E_s3.tail(25)

#%%
Emp_3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.3',
    ).loc[Employment].sum()

delta_Emp_3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.3',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_3_EU = delta_Emp_3.head(25)
delta_Emp_3_RoW = delta_Emp_3.tail(25)

#%%

VA_s3 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.3',
    ).loc[ValueAdded].sum()

delta_VA_s3 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.3",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s3_EU = delta_VA_s3.head(25)
delta_VA_s3_RoW = delta_VA_s3.tail(25)

#%% Intervention 4: Building with Steel weight optimization to Decrease 5% in Steel production 
path_s4 = "Scenarios_2/Intervention 2.4.xlsx" 
#data_exio.get_shock_excel(path=path_s4) 

#%%
data_exio.shock_calc(
    io= path_s4,
    z= True,
    scenario='Intervention 2.4',
    force_rewrite=True,
    notes=['Intervention 2.4'
           ])

#%%
CO2_s4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.4',
    ).loc[CO2_all].sum()

delta_E_s4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.4',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s4_EU = delta_E_s4.head(25)
delta_E_s4_RoW = delta_E_s4.tail(25)

#%%
Emp_4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.4',
    ).loc[Employment].sum()

delta_Emp_4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.4',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_4_EU = delta_Emp_4.head(25)
delta_Emp_4_RoW = delta_Emp_4.tail(25)

#%%

VA_s4 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.4',
    ).loc[ValueAdded].sum()

delta_VA_s4 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.4",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s4_EU = delta_VA_s4.head(25)
delta_VA_s4_RoW = delta_VA_s4.tail(25)

#%% Scenario 5: Re-manufacturing rebar waste 
# Intervention is the remanufacturing of rebar waste. This intervention could
# increase 10,5 % of the steel recycling. 

path_s5 = "Scenarios_2/Intervention 2.5.xlsx" 
#data_exio.get_shock_excel(path=path_s5) 
#%%
data_exio.shock_calc(
    io= path_s5,
    z= True,
    scenario='Intervention 2.5',
    force_rewrite=True,
    notes=['Intervention 2.5'
           ])
#%%
CO2_s5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.5',
    ).loc[CO2_all].sum()

delta_E_s5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.5',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s5_EU = delta_E_s5.head(25)
delta_E_s5_RoW = delta_E_s5.tail(25)
#%%
Emp_5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.5',
    ).loc[Employment].sum()
delta_Emp_5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.5',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_5_EU = delta_Emp_5.head(25)
delta_Emp_5_RoW = delta_Emp_5.tail(25)
#%%
VA_s5 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.5',
    ).loc[ValueAdded].sum()
delta_VA_s5 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.5",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s5_EU = delta_VA_s5.head(25)
delta_VA_s5_RoW = delta_VA_s5.tail(25)

#%% Scenario 6: 3D printing
# This intervention could potentially decrease 4,7% of the Steel production 
path_s6 = "Scenarios_2/Intervention 2.6.xlsx" 
#data_exio.get_shock_excel(path=path_s6) 
#%%
data_exio.shock_calc(
    io= path_s6,
    z= True,
    scenario='Intervention 2.6',
    force_rewrite=True,
    notes=['Intervention 2.6'
           ])
#%%
CO2_s6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.6',
    ).loc[CO2_all].sum()
delta_E_s6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.6',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s6_EU = delta_E_s6.head(25)
delta_E_s6_RoW = delta_E_s6.tail(25)

#%%
Emp_6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.6',
    ).loc[Employment].sum()
delta_Emp_6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.6',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_6_EU = delta_Emp_6.head(25)
delta_Emp_6_RoW = delta_Emp_6.tail(25)
#%%
VA_s6 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.6',
    ).loc[ValueAdded].sum()
delta_VA_s6 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.6",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s6_EU = delta_VA_s6.head(25)
delta_VA_s6_RoW = delta_VA_s6.tail(25)

#%% Scenario 7: Plastic deformation manufacturing
# This intervention could potentially increase recycling of aluminium by 2,6%  

path_s7 = "Scenarios_2/Intervention 2.7.xlsx" 
#data_exio.get_shock_excel(path=path_s7) 
#%%
data_exio.shock_calc(
    io= path_s7,
    z= True,
    scenario='Intervention 2.7',
    force_rewrite=True,
    notes=['Intervention 2.7'
           ])
#%%
CO2_s7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.7',
    ).loc[CO2_all].sum()
delta_E_s7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.7',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s7_EU = delta_E_s7.head(25)
delta_E_s7_RoW = delta_E_s7.tail(25)


#%%
Emp_7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.7',
    ).loc[Employment].sum()
delta_Emp_7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.7',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_7_EU = delta_Emp_7.head(25)
delta_Emp_7_RoW = delta_Emp_7.tail(25)
#%%
VA_s7 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.7',
    ).loc[ValueAdded].sum()
delta_VA_s7 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.7",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s7_EU = delta_VA_s7.head(25)
delta_VA_s7_RoW = delta_VA_s7.tail(25)

#%% Scenario 8: Pyrolysis to improve recycling efficiency for aluminium 
#%%
# This method could improve material efficiency by 0,7% of the total construction sector. 
# This could also decrease aluminium production with 0,7% 
path_s8 = "Scenarios_2/Intervention 2.8.xlsx" 
#data_exio.get_shock_excel(path=path_s8) 
#%%
data_exio.shock_calc(
    io= path_s8,
    z= True,
    scenario='Intervention 2.8',
    force_rewrite=True,
    notes=['Intervention 2.8'
           ])
#%%
CO2_s8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.8',
    ).loc[CO2_all].sum()
delta_E_s8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.8',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s8_EU = delta_E_s8.head(25)
delta_E_s8_RoW = delta_E_s8.tail(25)
#%%
Emp_8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.8',
    ).loc[Employment].sum()
delta_Emp_8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.8',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_8_EU = delta_Emp_8.head(25)
delta_Emp_8_RoW = delta_Emp_8.tail(25)
#%%
VA_s8 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.8',
    ).loc[ValueAdded].sum()
delta_VA_s8 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.8",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s8_EU = delta_VA_s8.head(25)
delta_VA_s8_RoW = delta_VA_s8.tail(25)

#%% Scenario 9: Adopting Design for Disassembly 
#%%
# This scenario could potentially decrease aluminium production with 3,5% 

path_s9 = "Scenarios_2/Intervention 2.9.xlsx" 
#data_exio.get_shock_excel(path=path_s9) 
#%%
data_exio.shock_calc(
    io= path_s9,
    z= True,
    scenario='Intervention 2.9',
    force_rewrite=True,
    notes=['Intervention 2.9'
           ])
#%%
CO2_s9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.9',
    ).loc[CO2_all].sum()
delta_E_s9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.9',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s9_EU = delta_E_s9.head(25)
delta_E_s9_RoW = delta_E_s9.tail(25)
#%%
Emp_9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.9',
    ).loc[Employment].sum()
delta_Emp_9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.9',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_9_EU = delta_Emp_9.head(25)
delta_Emp_9_RoW = delta_Emp_9.tail(25)
#%%
VA_s9 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.9',
    ).loc[ValueAdded].sum()
delta_VA_s9 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.9",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s9_EU = delta_VA_s9.head(25)
delta_VA_s9_RoW = delta_VA_s9.tail(25)


#%% Scenario 10: Small changes in Facade design
#%%
# This intervention could decrease the aluminium mass and therefore 
#production with 5,6% 

path_s10 = "Scenarios_2/Intervention 2.10.xlsx" 
#data_exio.get_shock_excel(path=path_s10) 
#%%
data_exio.shock_calc(
    io= path_s10,
    z= True,
    scenario='Intervention 2.10',
    force_rewrite=True,
    notes=['Intervention 2.10'
           ])
#%%
CO2_s10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.10',
    ).loc[CO2_all].sum()
delta_E_s10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.10',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()


delta_E_s10_EU = delta_E_s10.head(25)
delta_E_s10_RoW = delta_E_s10.tail(25)
#%%
Emp_10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.10',
    ).loc[Employment].sum()
delta_Emp_10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.10',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_10_EU = delta_Emp_10.head(25)
delta_Emp_10_RoW = delta_Emp_10.tail(25)
#%%
VA_s10 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.10',
    ).loc[ValueAdded].sum()
delta_VA_s10 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.10",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s10_EU = delta_VA_s10.head(25)
delta_VA_s10_RoW = delta_VA_s10.tail(25)

#%% Scenario 11: Using Recycled Aggregates of conventional ingredients 
#%%
# This intervention could potentially decrease manufacturing cement production 
# with 0,1%. 
path_s11 = "Scenarios_2/Intervention 2.11.xlsx" 
#data_exio.get_shock_excel(path=path_s11) 
#%%
data_exio.shock_calc(
    io= path_s11,
    z= True,
    scenario='Intervention 2.11',
    force_rewrite=True,
    notes=['Intervention 2.11'
           ])
#%%
CO2_s11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.11',
    ).loc[CO2_all].sum()
delta_E_s11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.11',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s11_EU = delta_E_s11.head(25)
delta_E_s11_RoW = delta_E_s11.tail(25)
#%%
Emp_11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.11',
    ).loc[Employment].sum()
delta_Emp_11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.11',
    base_scenario='baseline',
    type='absolute'
    ).loc[Employment].sum()

delta_Emp_11_EU = delta_Emp_11.head(25)
delta_Emp_11_RoW = delta_Emp_11.tail(25)
#%%
VA_s11 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.11',
    ).loc[ValueAdded].sum()
delta_VA_s11 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.11",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s11_EU = delta_VA_s11.head(25)
delta_VA_s11_RoW = delta_VA_s11.tail(25)

#%% Scenario 12: Using steel slag for cement properties
#%% 
# This intervention has a primary change of 4,3% of decrease in cement manufacturing
# and a secondary change of 4,3% increase in Steel recycling. 

path_s12 = "Scenarios_2/Intervention 2.12.xlsx" 
#data_exio.get_shock_excel(path=path_s12) 
#%%
data_exio.shock_calc(
    io= path_s12,
    z= True,
    scenario='Intervention 2.12',
    force_rewrite=True,
    notes=['Intervention 2.12'
           ])
#%%
CO2_s12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.12',
    ).loc[CO2_all].sum()
delta_E_s12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.12',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s12_EU = delta_E_s12.head(25)
delta_E_s12_RoW = delta_E_s12.tail(25)
#%%
Emp_12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.12',
    ).loc[Employment].sum()
delta_Emp_12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.12',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_12_EU = delta_Emp_12.head(25)
delta_Emp_12_RoW = delta_Emp_12.tail(25)
#%%
VA_s12 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.12',
    ).loc[ValueAdded].sum()
delta_VA_s12 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.12",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s12_EU = delta_VA_s12.head(25)
delta_VA_s12_RoW = delta_VA_s12.tail(25)

#%% Scenario 13: Using 3D printing to optimize concrete constructions
#%%
# This intervention could potentially decrease Concrete use by 14,4% in in the total
# construction sector. 
path_s13 = "Scenarios_2/Intervention 2.13.xlsx" 
#data_exio.get_shock_excel(path=path_s13) 
#%%
data_exio.shock_calc(
    io= path_s13,
    z= True,
    scenario='Intervention 2.13',
    force_rewrite=True,
    notes=['Intervention 2.13'
           ])
#%%
CO2_s13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.13',
    ).loc[CO2_all].sum()
delta_E_s13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.13',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s13_EU = delta_E_s13.head(25)
delta_E_s13_RoW = delta_E_s13.tail(25)
#%%
Emp_13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.13',
    ).loc[Employment].sum()
delta_Emp_13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.13',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_13_EU = delta_Emp_13.head(25)
delta_Emp_13_RoW = delta_Emp_13.tail(25)
#%%
VA_s13 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.13',
    ).loc[ValueAdded].sum()
delta_VA_s13 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.13",
    base_scenario="baseline",
    type='absolute'
    ).loc[(ValueAdded)].sum()

delta_VA_s13_EU = delta_VA_s13.head(25)
delta_VA_s13_RoW = delta_VA_s13.tail(25)

#%% Scenario 14: Using sustainable concrete by incorperating Aluminium dross and iron slag
#%%
# This intervention could potentially decrease concrete use by 18% in the entire construction industry
# As a secondary change it increase Re-processing aluminium and Re-processing Steel by 5% and 20%
path_s14 = "Scenarios_2/Intervention 2.14.xlsx" 
#data_exio.get_shock_excel(path=path_s14) 
#%%
data_exio.shock_calc(
    io= path_s14,
    z= True,
    scenario='Intervention 2.14',
    force_rewrite=True,
    notes=['Intervention 2.14'
           ])
#%%
CO2_s14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.14',
    ).loc[CO2_all].sum()
delta_E_s14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.14',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s14_EU = delta_E_s14.head(25)
delta_E_s14_RoW = delta_E_s14.tail(25)
#%%
Emp_14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.14',
    ).loc[Employment].sum()
delta_Emp_14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.14',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_14_EU = delta_Emp_14.head(25)
delta_Emp_14_RoW = delta_Emp_14.tail(25)
#%%
VA_s14 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.14',
    ).loc[ValueAdded].sum()
delta_VA_s14 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.14",
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

path_s15 = "Scenarios_2/Intervention 2.15.xlsx" 
#data_exio.get_shock_excel(path=path_s15) 
#%%
data_exio.shock_calc(
    io= path_s15,
    z= True,
    scenario='Intervention 2.15',
    force_rewrite=True,
    notes=['Intervention 2.15'
           ])
#%%
CO2_s15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.15',
    ).loc[CO2_all].sum()
delta_E_s15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.15',
    base_scenario='baseline',
    type='absolute',
    ).loc[CO2_all].sum()

delta_E_s15_EU = delta_E_s15.head(25)
delta_E_s15_RoW = delta_E_s15.tail(25)
#%%
Emp_15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.15',
    ).loc[Employment].sum()
delta_Emp_15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2.15',
    base_scenario='baseline',
    type='absolute',
    ).loc[Employment].sum()

delta_Emp_15_EU = delta_Emp_15.head(25)
delta_Emp_15_RoW = delta_Emp_15.tail(25)
#%%
VA_s15 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2.15',
    ).loc[ValueAdded].sum()
delta_VA_s15 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2.15",
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

intervention_names = [
    "Int1: Modular Design Steel",
    "Int2: Steel Scrap Diversion",
    "Int3: Improving yield steel",
    "Int4: Weigh Optimization Steel",
    "Int5: Rebar waste into nails",
    "Int6: 3D printing of steel",
    "Int7: Plastic deformation Aluminium",
    "Int8: Pyrolysis aluminium recycling",
    "Int9: Design for disassembly Aluminium",
    "Int10: Optimizing facade designs Aluminium",
    "Int11: Recycled aggregate concrete",
    "Int12: Reuse cement slag",
    "Int13: 3D printing Concrete",
    "Int14: Sustainable Concrete",
    "Int15: Fly ash as recycled cement"
]

#%%

# data = {
#     'Delta_E': delta_E_totals,
#     'Delta_Emp': delta_Emp_totals,
#     'Delta_VA': delta_VA_totals
# }

# # Convert to DataFrame
# df = pd.DataFrame(data)

# # Save to Excel
# df.to_excel('output.xlsx', index=False)

# print("Data saved to output.xlsx")

#%%
# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Create horizontal bar plot
y_pos = np.arange(len(delta_E_totals))
bars = ax.barh(y_pos, delta_E_totals, color='red', alpha=0.7)

# Add value annotations directly next to the bars
for i, v in enumerate(delta_E_totals):
    alignment = 'right' if v < 0 else 'left'  # Align text to the left or right of the bar
    plt.text(v, i, f'{v:,.2f}', va='center', ha=alignment, fontsize=10, 
             color='black', fontweight='bold')  # Bold black text for visibility

# # Add value labels
# for i, bar in enumerate(bars):
#     width = bar.get_width()
#     label_position = width if width >= 0 else width - 20000000
#     ax.text(label_position, bar.get_y() + bar.get_height()/2, 
#             f'{width:,.0f}', 
#             va='center', 
#             fontsize=8)

# Customize plot
ax.set_title("CO₂ Emissions Reduction from Baseline", 
             pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel("CO₂ Difference (metric kg)", fontsize=12)
ax.set_ylabel("All Interventions", fontsize=12)

# Set y-axis ticks
ax.set_yticks(y_pos)
ax.set_yticklabels([f'Intervention {i+1}' for i in range(len(delta_E_totals))])

# Add gridlines
ax.grid(True, linestyle='--', alpha=0.7, axis='x')

plt.tight_layout()
plt.savefig('emissions_reduction.png', dpi=300, bbox_inches='tight')
plt.show()

#%%

#%% Plotting the Employment changes per intervention in comparison with the baseline 

# Create figure
plt.figure(figsize=(14, 10))  # Increased figure size for better label visibility

# Create horizontal bar plot
y_pos = np.arange(len(delta_Emp_totals))
plt.barh(y_pos, delta_Emp_totals, color='navy', alpha=0.7)

# Add value annotations directly next to the bars
for i, v in enumerate(delta_Emp_totals):
    alignment = 'right' if v < 0 else 'left'  # Align text to the left or right of the bar
    plt.text(v, i, f'{v:,.2f}k', va='center', ha=alignment, fontsize=10, 
             color='black', fontweight='bold')  # Bold black text for visibility

# Customize plot
plt.title("Employment Changes from Baseline", 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel("Change in Employment", fontsize=12)
plt.ylabel("Interventions", fontsize=12)

# Set y-axis ticks with intervention names
plt.yticks(y_pos, intervention_names)

# Add gridlines
plt.grid(True, linestyle='--', alpha=0.7, axis='x')

# Adjust plot limits to accommodate labels
x_min, x_max = ax.get_xlim()
ax.set_xlim(x_min * 1.05, x_max * 1.05)  # Add 10% padding on both sides

# Adjust layout
plt.subplots_adjust(left=0.3, right=0.9)  # Increase margins on both sides
plt.tight_layout()

# Save and show plot
plt.savefig('employment_changes.png', dpi=300, bbox_inches='tight')
plt.show()


#%% Plotting the changes of CO2 emissions 

# Create figure
fig, ax = plt.subplots(figsize=(14, 9))  # Increased figure size to accommodate longer labels

# Convert values to millions
delta_E_millions = [x / 1_000_000 for x in delta_E_totals]

# Create horizontal bar plot
y_pos = np.arange(len(delta_E_millions))
bars = ax.barh(y_pos, delta_E_millions, color='red', alpha=0.7)

# Add value annotations directly next to the bars
for i, v in enumerate(delta_E_millions):
    alignment = 'right' if v < 0 else 'left'  # Align text to the left or right of the bar
    plt.text(v, i, f'{v:,.2f}M', va='center', ha=alignment, fontsize=10, 
             color='black', fontweight='bold')  # Bold black text for visibility

# Customize plot
ax.set_title("CO₂ Emissions Reduction from Baseline", 
             pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel("CO₂ Difference (million kg)", fontsize=12)
ax.set_ylabel("Interventions", fontsize=12)

# Set y-axis ticks with intervention names
ax.set_yticks(y_pos)
ax.set_yticklabels(intervention_names)

# Add gridlines
ax.grid(True, linestyle='--', alpha=0.7, axis='x')

# Adjust layout for better label visibility
plt.subplots_adjust(left=0.3)  # Increase left margin to accommodate long labels
plt.tight_layout()

# Save and show plot
plt.savefig('emissions_reduction.png', dpi=300, bbox_inches='tight')
plt.show()

#%%

# Create figure with more height for better spacing
fig, ax = plt.subplots(figsize=(16, 12))  # Increased figure size further

# Convert values to millions
delta_E_millions = [x / 1_000_000 for x in delta_E_totals]

# Create horizontal bar plot
y_pos = np.arange(len(delta_E_millions))
bars = ax.barh(y_pos, delta_E_millions, color='red', alpha=0.7)

# Calculate the maximum absolute value for padding
max_abs_value = max(abs(min(delta_E_millions)), abs(max(delta_E_millions)))
padding = max_abs_value * 0.02  # 2% padding

# Add value annotations with adjusted positioning
for i, v in enumerate(delta_E_millions):
    # Determine text position and alignment
    if v < 0:
        text_pos = v - padding
        alignment = 'right'
    else:
        text_pos = v + padding
        alignment = 'left'
        
    plt.text(text_pos, i, f'{v:,.2f}M', 
             va='center', 
             ha=alignment, 
             fontsize=10,
             color='black',
             fontweight='bold')

# Customize plot
ax.set_title("CO₂ Emissions Reduction from Baseline", 
             pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel("CO₂ Difference (million kg)", fontsize=12)
ax.set_ylabel("Interventions", fontsize=12)

# Set y-axis ticks with intervention names
ax.set_yticks(y_pos)
ax.set_yticklabels(intervention_names)

# Add gridlines
ax.grid(True, linestyle='--', alpha=0.7, axis='x')

# Adjust plot limits to accommodate labels
x_min, x_max = ax.get_xlim()
ax.set_xlim(x_min * 1.05, x_max * 1.05)  # Add 10% padding on both sides

# Adjust layout
plt.subplots_adjust(left=0.3, right=0.9)  # Increase margins on both sides
plt.tight_layout()

# Save and show plot
plt.savefig('emissions_reduction.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
plt.show()

#%%

# Create figure with more height for better spacing
fig, ax = plt.subplots(figsize=(16, 12))  # Increased figure size for better visibility

# Create horizontal bar plot
y_pos = np.arange(len(delta_VA_totals))
bars = ax.barh(y_pos, delta_VA_totals, color='orange', alpha=0.7)

# Calculate the maximum absolute value for padding
max_abs_value = max(abs(min(delta_VA_totals)), abs(max(delta_VA_totals)))
padding = max_abs_value * 0.02  # 2% padding

# Add value annotations with adjusted positioning
for i, v in enumerate(delta_VA_totals):
    # Determine text position and alignment
    if v < 0:
        text_pos = v - padding
        alignment = 'right'
    else:
        text_pos = v + padding
        alignment = 'left'
        
    ax.text(text_pos, i, f'{v:,.2f}M€', 
            va='center', 
            ha=alignment, 
            fontsize=10,
            color='black',
            fontweight='bold')

# Customize plot
ax.set_title("Value Added Changes from Baseline", 
             pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel("Change in Value Added (Million €)", fontsize=12)
ax.set_ylabel("Interventions", fontsize=12)

# Set y-axis ticks with intervention names
ax.set_yticks(y_pos)
ax.set_yticklabels(intervention_names)

# Add gridlines
ax.grid(True, linestyle='--', alpha=0.7, axis='x')

# Adjust plot limits to accommodate labels
x_min, x_max = ax.get_xlim()
ax.set_xlim(x_min * 1.1, x_max * 1.1)  # Add 10% padding on both sides

# Adjust layout
plt.subplots_adjust(left=0.3, right=0.9)  # Increase margins on both sides
plt.tight_layout()

# Save and show plot
plt.savefig('value_added_changes.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
plt.show()
#%% Plotting the Value Added changes per intervention 

delta_VA_totals = [
    441.8022859, -69.66453618, -386.48829, -355.381422, -149.2811376,
    -345.2276694, 95.95976738, 2.027421375, -0.263510378, -0.003736317,
    -19.32067971, 53.66318678, 181.4532891, 125.3632053, -167.1392149
]

# Create figure
plt.figure(figsize=(14, 10))

# Create horizontal bar plot
y_pos = np.arange(len(delta_VA_totals))
plt.barh(y_pos, delta_VA_totals, color='orange', alpha=0.7)

# Add value annotations directly next to the bars
for i, v in enumerate(delta_VA_totals):
    alignment = 'right' if v < 0 else 'left'  # Align text to the left or right of the bar
    plt.text(v, i, f'{v:,.2f}M€', va='center', ha=alignment, fontsize=10, 
             color='black', fontweight='bold')

# Customize plot
plt.title("Value Added Changes from Baseline", 
          pad=20, fontsize=14, fontweight='bold')
plt.xlabel("Change in Value Added (Million €)", fontsize=12)
plt.ylabel("Interventions", fontsize=12)

# Set y-axis ticks with intervention names
plt.yticks(y_pos, intervention_names)

# Add gridlines
plt.grid(True, linestyle='--', alpha=0.7, axis='x')

# Adjust plot limits to accommodate labels
x_min, x_max = ax.get_xlim()
ax.set_xlim(x_min * 1.1, x_max * 1.1)  # Add 10% padding on both sides

# Adjust layout
plt.subplots_adjust(left=0.3, right=0.9)  # Increase margins on both sides
plt.tight_layout()

# Save and show plot
plt.savefig('value_added_changes.png', dpi=300, bbox_inches='tight')
plt.show()
#%%

# Initialize dictionaries for RoW and EU data
highest_impact_sectors_RoW = {}
highest_impact_values_RoW = {}
highest_impact_sectors_EU = {}
highest_impact_values_EU = {}

for i in range(1, 16):
    # Process RoW data
    delta_E_RoW = globals()[f"delta_E_s{i}_RoW"]
    highest_impact_sector_RoW = delta_E_RoW.abs().idxmax()
    highest_impact_value_RoW = delta_E_RoW[highest_impact_sector_RoW]
    highest_impact_sectors_RoW[f"s{i}"] = highest_impact_sector_RoW
    highest_impact_values_RoW[f"s{i}"] = highest_impact_value_RoW

    # Process EU data
    delta_E_EU = globals()[f"delta_E_s{i}_EU"]
    highest_impact_sector_EU = delta_E_EU.abs().idxmax()
    highest_impact_value_EU = delta_E_EU[highest_impact_sector_EU]
    highest_impact_sectors_EU[f"s{i}"] = highest_impact_sector_EU
    highest_impact_values_EU[f"s{i}"] = highest_impact_value_EU

# Convert the dictionaries to DataFrames
sectors_table_RoW = pd.DataFrame(list(highest_impact_sectors_RoW.items()), columns=["Scenario", "Highest Impact Sector (RoW)"])
sectors_table_EU = pd.DataFrame(list(highest_impact_sectors_EU.items()), columns=["Scenario", "Highest Impact Sector (EU)"])

# Merge the DataFrames for better comparison
sectors_table = pd.merge(sectors_table_RoW, sectors_table_EU, on="Scenario")

# Create a table with Matplotlib
fig, ax = plt.subplots(figsize=(10, 5))

# Hide the axes
ax.axis('tight')
ax.axis('off')

# Prepare the data for the table
table_data = [list(sectors_table.columns)] + sectors_table.values.tolist()

# Add the table to the plot
table = ax.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.2, 0.4, 0.4])

# Enhance table appearance
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([0, 1, 2])

# Display the plot
plt.show()

# Save the merged DataFrame to an Excel file
sectors_table.to_excel("highest_impact_sectors_comparison.xlsx", index=False)

print("Data has been saved to 'highest_impact_sectors_comparison.xlsx'.")
#%%

# Initialize dictionaries for RoW and EU data
top_3_sectors_RoW = {}
top_3_sectors_EU = {}

for i in range(1, 16):
    # Process RoW data
    delta_E_RoW = globals()[f"delta_E_s{i}_RoW"]
    top_3_RoW = delta_E_RoW.abs().nlargest(3).index.tolist()
    top_3_values_RoW = delta_E_RoW[top_3_RoW].values.tolist()
    top_3_sectors_RoW[f"s{i}"] = list(zip(top_3_RoW, top_3_values_RoW))

    # Process EU data
    delta_E_EU = globals()[f"delta_E_s{i}_EU"]
    top_3_EU = delta_E_EU.abs().nlargest(3).index.tolist()
    top_3_values_EU = delta_E_EU[top_3_EU].values.tolist()
    top_3_sectors_EU[f"s{i}"] = list(zip(top_3_EU, top_3_values_EU))

# Prepare data for plotting
plot_data = []
for scenario in top_3_sectors_RoW.keys():
    row = [scenario]
    row += [f"{sector} ({value:.2f})" for sector, value in top_3_sectors_RoW[scenario]]
    row += [f"{sector} ({value:.2f})" for sector, value in top_3_sectors_EU[scenario]]
    plot_data.append(row)

# Create a DataFrame for easier plotting
columns = ["Scenario"] + [f"Top {i} (RoW)" for i in range(1, 4)] + [f"Top {i} (EU)" for i in range(1, 4)]
sectors_df = pd.DataFrame(plot_data, columns=columns)

# Plot the table using Matplotlib
fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('tight')
ax.axis('off')

# Add the table to the plot
table = ax.table(cellText=sectors_df.values, colLabels=sectors_df.columns, loc='center', cellLoc='center')

# Enhance table appearance
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(range(len(columns)))

# Display the plot
plt.show()

# Save the data to an Excel file
sectors_df.to_excel("top_3_sectors_clear.xlsx", index=False)

print("Top 3 sector data has been saved to 'top_3_sectors_clear.xlsx'.")

#%%

from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Example data (replace with your actual data)
delta_E_totals = [-117423057.3, -35516080.36, -364330667.9, -261504734.9, 
                  -7610589.044, -239377416.2, -3455549.736, -294396.2818, 
                  -1426689.687, -7442722.482, -32008990.82, 17432160.44, 
                  -300243948.9, -43676056.62, -297534563.5]
delta_Emp_totals = [9114.687303, -1795.646081, -8758.69875, -8103.213209, 
                    -3847.812739, -7871.692884, 1852.65913, 29.11293018, 
                    -5.233697598, -225.4050111, -389.5320335, 1184.360868, 
                    3366.41353, 2890.169701, -3411.73282]
delta_VA_totals = [441802285.9, -69664536.18, -386488290, -355381422, 
                   -149281137.6, -345227669.4, 95959767.38, 2027421.375, 
                   -263510.3783, -3736.317347, -19320679.71, 53663186.78, 
                   181453289.1, 125363205.3, -167139214.9]

# Create a DataFrame
data = {
    'Intervention': [f'Intervention {i+1}' for i in range(15)],
    'Delta Emissions (kg)': delta_E_totals,
    'Delta Employment': delta_Emp_totals,
    'Delta Value-Added (€)': delta_VA_totals
}

df = pd.DataFrame(data)

# Normalize the data to a range of [0, 1]
emissions_norm = Normalize(vmin=np.min(df['Delta Emissions (kg)']), vmax=np.max(df['Delta Emissions (kg)']))
employment_norm = Normalize(vmin=np.min(df['Delta Employment']), vmax=np.max(df['Delta Employment']))
value_added_norm = Normalize(vmin=np.min(df['Delta Value-Added (€)']), vmax=np.max(df['Delta Value-Added (€)']))

# Define a colormap: 'coolwarm' from dark red to blue
emissions_cmap = ScalarMappable(norm=emissions_norm, cmap='coolwarm')
employment_cmap = ScalarMappable(norm=employment_norm, cmap='coolwarm')
value_added_cmap = ScalarMappable(norm=value_added_norm, cmap='coolwarm')

# Plotting the table with color distribution
fig, ax = plt.subplots(figsize=(12, 8))  # Adjust the size of the plot
ax.axis('off')

# Create the table with conditional coloring
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=['#f2f2f2']*df.shape[1])

# Apply color to each cell based on the value using colormap
for i in range(df.shape[0]):
    # Emissions column
    color = emissions_cmap.to_rgba(df.iloc[i, 1])  # Get color based on value
    table[(i+1, 1)].set_facecolor(color)
    
    # Employment column
    color = employment_cmap.to_rgba(df.iloc[i, 2])  # Get color based on value
    table[(i+1, 2)].set_facecolor(color)
    
    # Value Added column
    color = value_added_cmap.to_rgba(df.iloc[i, 3])  # Get color based on value
    table[(i+1, 3)].set_facecolor(color)

# Style the table (optional)
table.auto_set_font_size(False)  # Prevent automatic font size adjustment
table.set_fontsize(12)  # Set the font size for the table
table.scale(1.2, 1.2)  # Scale the table (make it bigger or smaller)

# Show the plot
plt.title("Intervention Table with Enhanced Conditional Coloring", fontsize=14)
plt.show()
