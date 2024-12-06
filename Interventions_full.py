# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 18:38:18 2024

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
path_aggr = 'Aggregations/aggregation_data.xlsx'
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

#%% Calculation Intervention 1, Steel :
    # Intervention: Modular Design could give a 10.5% decrease in manufacturing of basic iron and steel 

path_s1 = "Scenarios/Intervention1.xlsx" 
#data_exio.get_shock_excel(path=path_s1) 
#%%

data_exio.shock_calc(
    io= path_s1,
    z= True,
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


#%% Value Added shock calculations Intervention 1 

VA_s1 = data_exio.query(
    matrices='V',
    scenarios='Intervention 1',
    ).loc[ValueAdded].sum()

VA_baseline = data_exio.query(
    matrices='V',
    scenarios='baseline',
    ).loc[(ValueAdded)].sum()

delta_VA_s1 = data_exio.query(
    matrices="V",
    scenarios="Intervention 1",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()


#%% Calculation Scenario 2: Scrap Diversion 
#%% Calculation Intervention 2, Steel :
    # Intervention:Scrap diversion could reduce 14% of the scrap in construction 
    # which is 35% of the steel market. Which is a decrease of 4,9%

path_s2 = "Scenarios/Intervention2.xlsx" 
#data_exio.get_shock_excel(path=path_s2) 

#%%
data_exio.shock_calc(
    io= path_s2,
    z= True,
    scenario='Intervention 2',
    force_rewrite=True,
    notes=['Intervention 2'
           ])

#%% CO2 shock calculations scenario 2
CO2_s2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2',
    ).loc['CO2 - combustion - air'].sum()

delta_E_s2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']


#%%
Emp_2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2',
    ).loc[Employment].sum()

delta_Emp_2 = data_exio.query(
    matrices='E',
    scenarios='Intervention 2',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()


#%%

VA_s2 = data_exio.query(
    matrices='V',
    scenarios='Intervention 2',
    ).loc[ValueAdded].sum()

delta_VA_s2 = data_exio.query(
    matrices="V",
    scenarios="Intervention 2",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()


#%% Scenario 3: Improvement of Yield scrap 
#%% Intervention: Reduction of scrap in the manufacturing process of steel. 
# Could decrease 26% of steel manufacturing, + MP. Decrease of 9,1% 
path_s3 = "Scenarios/Intervention3.xlsx" 
#data_exio.get_shock_excel(path=path_s3) 

#%%
data_exio.shock_calc(
    io= path_s3,
    z= True,
    scenario='Intervention 3',
    force_rewrite=True,
    notes=['Intervention 3'
           ])

#%%
CO2_s3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 3',
    ).loc['CO2 - combustion - air'].sum()

delta_E_s3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 3',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']

#%%
Emp_3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 3',
    ).loc[Employment].sum()

delta_Emp_3 = data_exio.query(
    matrices='E',
    scenarios='Intervention 3',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()

#%%

VA_s3 = data_exio.query(
    matrices='V',
    scenarios='Intervention 3',
    ).loc[ValueAdded].sum()

delta_VA_s3 = data_exio.query(
    matrices="V",
    scenarios="Intervention 3",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Intervention 4: Building with weight optimization to Decrease 5% in Steel production 
path_s4 = "Scenarios/Intervention4.xlsx" 
#data_exio.get_shock_excel(path=path_s4) 

#%%
data_exio.shock_calc(
    io= path_s4,
    z= True,
    scenario='Intervention 4',
    force_rewrite=True,
    notes=['Intervention 4'
           ])

#%%
CO2_s4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 4',
    ).loc['CO2 - combustion - air'].sum()

delta_E_s4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 4',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']

#%%
Emp_4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 4',
    ).loc[Employment].sum()

delta_Emp_4 = data_exio.query(
    matrices='E',
    scenarios='Intervention 4',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()

#%%

VA_s4 = data_exio.query(
    matrices='V',
    scenarios='Intervention 4',
    ).loc[ValueAdded].sum()

delta_VA_s4 = data_exio.query(
    matrices="V",
    scenarios="Intervention 4",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 5: Re-manufacturing rebar waste 
# Intervention is the remanufacturing of rebar waste. This intervention could
# increase 10,5 % of the steel recycling. 

path_s5 = "Scenarios/Intervention5.xlsx" 
#data_exio.get_shock_excel(path=path_s5) 
#%%
data_exio.shock_calc(
    io= path_s5,
    z= True,
    scenario='Intervention 5',
    force_rewrite=True,
    notes=['Intervention 5'
           ])
#%%
CO2_s5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 5',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 5',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 5',
    ).loc[Employment].sum()
delta_Emp_5 = data_exio.query(
    matrices='E',
    scenarios='Intervention 5',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s5 = data_exio.query(
    matrices='V',
    scenarios='Intervention 5',
    ).loc[ValueAdded].sum()
delta_VA_s5 = data_exio.query(
    matrices="V",
    scenarios="Intervention 5",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 6: 3D printing
# This intervention could potentially decrease 4,7% of the Steel production 
path_s6 = "Scenarios/Intervention6.xlsx" 
#data_exio.get_shock_excel(path=path_s6) 
#%%
data_exio.shock_calc(
    io= path_s6,
    z= True,
    scenario='Intervention 6',
    force_rewrite=True,
    notes=['Intervention 6'
           ])
#%%
CO2_s6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 6',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 6',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 6',
    ).loc[Employment].sum()
delta_Emp_6 = data_exio.query(
    matrices='E',
    scenarios='Intervention 6',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s6 = data_exio.query(
    matrices='V',
    scenarios='Intervention 6',
    ).loc[ValueAdded].sum()
delta_VA_s6 = data_exio.query(
    matrices="V",
    scenarios="Intervention 6",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 7: Plastic deformation manufacturing
# This intervention could potentially increase recycling of aluminium by 0,6%  

path_s7 = "Scenarios/Intervention7.xlsx" 
#data_exio.get_shock_excel(path=path_s7) 
#%%
data_exio.shock_calc(
    io= path_s7,
    z= True,
    scenario='Intervention 7',
    force_rewrite=True,
    notes=['Intervention 7'
           ])
#%%
CO2_s7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 7',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 7',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 7',
    ).loc[Employment].sum()
delta_Emp_7 = data_exio.query(
    matrices='E',
    scenarios='Intervention 7',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s7 = data_exio.query(
    matrices='V',
    scenarios='Intervention 7',
    ).loc[ValueAdded].sum()
delta_VA_s7 = data_exio.query(
    matrices="V",
    scenarios="Intervention 7",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 8: Pyrolysis to improve recycling efficiency for aluminium 
#%%
# This method could improve material efficiency by 0,7% of the total construction sector. 
# This could also decrease aluminium production with 0,7% 
path_s8 = "Scenarios/Intervention8.xlsx" 
#data_exio.get_shock_excel(path=path_s8) 
#%%
data_exio.shock_calc(
    io= path_s8,
    z= True,
    scenario='Intervention 8',
    force_rewrite=True,
    notes=['Intervention 8'
           ])
#%%
CO2_s8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 8',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 8',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 8',
    ).loc[Employment].sum()
delta_Emp_8 = data_exio.query(
    matrices='E',
    scenarios='Intervention 8',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s8 = data_exio.query(
    matrices='V',
    scenarios='Intervention 8',
    ).loc[ValueAdded].sum()
delta_VA_s8 = data_exio.query(
    matrices="V",
    scenarios="Intervention 8",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 9: Adopting Design for Disassembly 
#%%
# This scenario could potentially decrease aluminium production with 3,5% 

path_s9 = "Scenarios/Intervention9.xlsx" 
#data_exio.get_shock_excel(path=path_s9) 
#%%
data_exio.shock_calc(
    io= path_s9,
    z= True,
    scenario='Intervention 9',
    force_rewrite=True,
    notes=['Intervention 9'
           ])
#%%
CO2_s9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 9',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 9',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 9',
    ).loc[Employment].sum()
delta_Emp_9 = data_exio.query(
    matrices='E',
    scenarios='Intervention 9',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s9 = data_exio.query(
    matrices='V',
    scenarios='Intervention 9',
    ).loc[ValueAdded].sum()
delta_VA_s9 = data_exio.query(
    matrices="V",
    scenarios="Intervention 9",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 10: Small changes in Facade design
#%%
# This intervention could decrease the aluminium mass and therefore 
#production with 5,6% 

path_s10 = "Scenarios/Intervention10.xlsx" 
#data_exio.get_shock_excel(path=path_s10) 
#%%
data_exio.shock_calc(
    io= path_s10,
    z= True,
    scenario='Intervention 10',
    force_rewrite=True,
    notes=['Intervention 10'
           ])
#%%
CO2_s10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 10',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 10',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 10',
    ).loc[Employment].sum()
delta_Emp_10 = data_exio.query(
    matrices='E',
    scenarios='Intervention 10',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s10 = data_exio.query(
    matrices='V',
    scenarios='Intervention 10',
    ).loc[ValueAdded].sum()
delta_VA_s10 = data_exio.query(
    matrices="V",
    scenarios="Intervention 10",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 11: Using Recycled Aggregates of conventional ingredients 
#%%
# This intervention could potentially decrease manufacturing cement production 
# with 0,1%. 
path_s11 = "Scenarios/Intervention11.xlsx" 
#data_exio.get_shock_excel(path=path_s11) 
#%%
data_exio.shock_calc(
    io= path_s11,
    z= True,
    scenario='Intervention 11',
    force_rewrite=True,
    notes=['Intervention 11'
           ])
#%%
CO2_s11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 11',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 11',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 11',
    ).loc[Employment].sum()
delta_Emp_11 = data_exio.query(
    matrices='E',
    scenarios='Intervention 11',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s11 = data_exio.query(
    matrices='V',
    scenarios='Intervention 11',
    ).loc[ValueAdded].sum()
delta_VA_s11 = data_exio.query(
    matrices="V",
    scenarios="Intervention 11",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 12: Using steel slag for cement properties
#%% 
# This intervention has a primary change of 4,3% of decrease in cement manufacturing
# and a secondary change of 4,3% increase in Steel recycling. 

path_s12 = "Scenarios/Intervention12.xlsx" 
#data_exio.get_shock_excel(path=path_s12) 
#%%
data_exio.shock_calc(
    io= path_s12,
    z= True,
    scenario='Intervention 12',
    force_rewrite=True,
    notes=['Intervention 12'
           ])
#%%
CO2_s12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 12',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 12',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 12',
    ).loc[Employment].sum()
delta_Emp_12 = data_exio.query(
    matrices='E',
    scenarios='Intervention 12',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s12 = data_exio.query(
    matrices='V',
    scenarios='Intervention 12',
    ).loc[ValueAdded].sum()
delta_VA_s12 = data_exio.query(
    matrices="V",
    scenarios="Intervention 12",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 13: Using 3D printing to optimize concrete constructions
#%%
# This intervention could potentially decrease Concrete use by 14,4% in in the total
# construction sector. 
path_s13 = "Scenarios/Intervention13.xlsx" 
#data_exio.get_shock_excel(path=path_s13) 
#%%
data_exio.shock_calc(
    io= path_s13,
    z= True,
    scenario='Intervention 13',
    force_rewrite=True,
    notes=['Intervention 13'
           ])
#%%
CO2_s13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 13',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 13',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 13',
    ).loc[Employment].sum()
delta_Emp_13 = data_exio.query(
    matrices='E',
    scenarios='Intervention 13',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s13 = data_exio.query(
    matrices='V',
    scenarios='Intervention 13',
    ).loc[ValueAdded].sum()
delta_VA_s13 = data_exio.query(
    matrices="V",
    scenarios="Intervention 13",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 14: Using sustainable concrete by incorperating Aluminium dross and iron slag
#%%
# This intervention could potentially decrease concrete use by 18% in the entire construction industry
# As a secondary change it increase Re-processing aluminium and Re-processing Steel by 5% and 20%
path_s14 = "Scenarios/Intervention14.xlsx" 
#data_exio.get_shock_excel(path=path_s14) 
#%%
data_exio.shock_calc(
    io= path_s14,
    z= True,
    scenario='Intervention 14',
    force_rewrite=True,
    notes=['Intervention 14'
           ])
#%%
CO2_s14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 14',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 14',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 14',
    ).loc[Employment].sum()
delta_Emp_14 = data_exio.query(
    matrices='E',
    scenarios='Intervention 14',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s14 = data_exio.query(
    matrices='V',
    scenarios='Intervention 14',
    ).loc[ValueAdded].sum()
delta_VA_s14 = data_exio.query(
    matrices="V",
    scenarios="Intervention 14",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()

#%% Scenario 15: Using Fly ash as a recycled aggregate for cement 
#%%
# This intervention increases the Re-processing of Fly ash into clinker by 13,75%
# As secondary changes it could have a decrease in landfill of waste by 19,1% and 
# decrease Concrete manufacturing by 13,75%.  

path_s15 = "Scenarios/Intervention15.xlsx" 
#data_exio.get_shock_excel(path=path_s15) 
#%%
data_exio.shock_calc(
    io= path_s15,
    z= True,
    scenario='Intervention 15',
    force_rewrite=True,
    notes=['Intervention 15'
           ])
#%%
CO2_s15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 15',
    ).loc['CO2 - combustion - air'].sum()
delta_E_s15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 15',
    base_scenario='baseline',
    type='relative',
    ).loc['CO2 - combustion - air']
#%%
Emp_15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 15',
    ).loc[Employment].sum()
delta_Emp_15 = data_exio.query(
    matrices='E',
    scenarios='Intervention 15',
    base_scenario='baseline',
    type='relative',
    ).loc[Employment].sum()
#%%
VA_s15 = data_exio.query(
    matrices='V',
    scenarios='Intervention 15',
    ).loc[ValueAdded].sum()
delta_VA_s15 = data_exio.query(
    matrices="V",
    scenarios="Intervention 15",
    base_scenario="baseline",
    type='relative'
    ).loc[(ValueAdded)].sum()


#%% Plots Intervention 1

#%% Plots CO2 intervention 1 

delta_E_s1_EU = delta_E_s1.head(16).sort_values(ascending=True)
delta_E_s1_EU.plot(kind='bar', color='red') 
plt.title("Delta CO2 of the EU")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()


delta_E_s1_RoW = delta_E_s1.tail(16).sort_values(ascending=True)
delta_E_s1_RoW.plot(kind='bar', color='red') 
plt.title("Delta CO2 of the Rest of the World")
plt.xlabel("index")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()

#%% Plots for Employment Intervention 1

delta_Emp_1_EU = delta_Emp_1.head(16).sort_values(ascending=True)
delta_Emp_1_EU.plot(kind='bar', color='red') 
plt.title("Delta employment of the EU")
plt.xlabel("Sectors")
plt.ylabel("Employment delta with the baseline in M.hr")
plt.grid(True)
plt.show()

delta_Emp_1_RoW = delta_Emp_1.tail(16).sort_values(ascending=True)
delta_Emp_1_RoW.plot(kind='bar', color='red') 
plt.title("Delta employment of the Rest of the World")
plt.xlabel("Sectors")
plt.ylabel("Employment difference with the baseline in M.hr")
plt.grid(True)

plt.show()
plt.tight_layout(rect=[0, 0.03, 1, 0.095])

#%% Plots for Value Added Intervention 1

delta_VA_s1_EU = delta_VA_s1.head(16).sort_values(ascending=True)
delta_VA_s1_EU.plot(kind='bar', color='red')
plt.title("Delta Value Added of the EU")
plt.xlabel("Sectors")
plt.ylabel("Value Added difference with the baseline")
plt.grid(True)
plt.show()

delta_VA_s1_RoW = delta_VA_s1.tail(16).sort_values(ascending=True)
delta_VA_s1_RoW.plot(kind='bar', color='red')
plt.title("Delta Value Added of the RoW")
plt.xlabel("Sectors")
plt.ylabel("Value Added difference with the baseline")
plt.grid(True)
plt.show()

plt.show()
plt.tight_layout(rect=[0, 0.03, 1, 0.095])

#%% Plots CO2 intervention 2
delta_E_s2_EU = delta_E_s2.head(16).sort_values(ascending=True)
delta_E_s2_EU.plot(kind='bar', color='red') 
plt.title("Int2: Delta CO2 of the EU")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()

delta_E_s2_RoW = delta_E_s2.tail(16).sort_values(ascending=True)
delta_E_s2_RoW.plot(kind='bar', color='red') 
plt.title("Int2: Delta CO2 of the Rest of the World")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()
#%% Plots for Employment Intervention 2
delta_Emp_2_EU = delta_Emp_2.head(16).sort_values(ascending=True)
delta_Emp_2_EU.plot(kind='bar', color='red') 
plt.title("Delta employment of the EU")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()
delta_Emp_2_RoW = delta_Emp_2.tail(16).sort_values(ascending=True)
delta_Emp_2_RoW.plot(kind='bar', color='red') 
plt.title("Delta employment of the Rest of the World")
plt.xlabel("Sectors")
plt.ylabel("Employment difference with the baseline")
plt.grid(True)
plt.show()
plt.tight_layout(rect=[0, 0.03, 1, 0.095])
#%% Plots for Value Added Intervention 2
delta_VA_s2_EU = delta_VA_s2.head(16).sort_values(ascending=True)
delta_VA_s2_EU.plot(kind='bar', color='red')
plt.title("Delta Value Added of the EU")
plt.xlabel("Sectors")
plt.ylabel("Value Added difference with the baseline")
plt.grid(True)
plt.show()

delta_VA_s2_RoW = delta_VA_s2.tail(16).sort_values(ascending=True)
delta_VA_s2_RoW.plot(kind='bar', color='red')
plt.title("Delta Value Added of the RoW")
plt.xlabel("Sectors")
plt.ylabel("Value Added difference with the baseline")
plt.grid(True)
plt.show()
plt.show()
plt.tight_layout(rect=[0, 0.03, 1, 0.095])

#%% Plots CO2 intervention 3
delta_E_s3_EU = delta_E_s3.head(16).sort_values(ascending=True)
delta_E_s3_EU.plot(kind='bar', color='red') 
plt.title("Int3: Delta CO2 of the EU")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()

delta_E_s3_RoW = delta_E_s3.tail(16).sort_values(ascending=True)
delta_E_s3_RoW.plot(kind='bar', color='red') 
plt.title("Int3: Delta CO2 of the Rest of the World")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()
#%% Plots for Employment Intervention 3
delta_Emp_3_EU = delta_Emp_3.head(16).sort_values(ascending=True)
delta_Emp_3_EU.plot(kind='bar', color='red') 
plt.title("Int3: Delta employment of the EU")
plt.xlabel("Sectors")
plt.ylabel("CO2 difference with the baseline")
plt.grid(True)
plt.show()
delta_Emp_3_RoW = delta_Emp_3.tail(16).sort_values(ascending=True)
delta_Emp_3_RoW.plot(kind='bar', color='red') 
plt.title("Int3: Delta employment of the Rest of the World")
plt.xlabel("Sectors")
plt.ylabel("Employment difference with the baseline")
plt.grid(True)
plt.show()
plt.tight_layout(rect=[0, 0.03, 1, 0.095])
#%% Plots for Value Added Intervention 3
delta_VA_s3_EU = delta_VA_s3.head(16).sort_values(ascending=True)
delta_VA_s3_EU.plot(kind='bar', color='red')
plt.title("Int3: Delta Value Added of the EU")
plt.xlabel("Sectors")
plt.ylabel("Value Added difference with the baseline")
plt.grid(True)
plt.show()
delta_VA_s3_RoW = delta_VA_s3.tail(16).sort_values(ascending=True)
delta_VA_s3_RoW.plot(kind='bar', color='red')
plt.title("Int3: Delta Value Added of the RoW")
plt.xlabel("Sectors")
plt.ylabel("Value Added difference with the baseline")
plt.grid(True)
plt.show()
plt.show()
plt.tight_layout(rect=[0, 0.03, 1, 0.095])


#%% Checking changes
data_exio.meta_history


# Important commands

#CoreModel.meta_history
#CoreModel.add_note(notes)
#CoreModel.search(item, search, ignore_case=True)

# Checking Parameters

# Y = exiobase.Y # Final demand
# Z = exiobase.Z # Intermediate demand matrix
# A = exiobase.z # A-matrix
# E = exiobase.E # Satellite transaction flows matrix
# e = exiobase.e # Satellitte transaction coefficient matrix
# L = exiobase.w # L-matrix
