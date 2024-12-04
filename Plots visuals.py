#Code Thesis Intervention 1

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

#%%
data_exio.V
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

#%% Value Added shock calculations Intervention 1 
ValueAdded = ['Taxes less subsidies on products purchased: Total',
'Other net taxes on production',
"Compensation of employees; wages, salaries, & employers' social contributions: Low-skilled",
"Compensation of employees; wages, salaries, & employers' social contributions: Medium-skilled",
"Compensation of employees; wages, salaries, & employers' social contributions: High-skilled",
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




#%% CO2 plot

CO2_s1.plot_matrix('E','Regions','red',y='Value',item='Sector',facet_row='CO2_emissions')


#%% MARIO matrix plot 
delta_E_s1.plot(kind="bar", x='Region')
delta_VA_s1.plot(kind="bar")


#%%

df = delta_VA_s1.unstack()

plt.figure(figsize=(15,8))

bar_width = 0.35 
sectors = df.columns
index = range(len(sectors))

plt.bar([i for i in index], df.loc['EU'], bar_width, label='EU', color='blue')
plt.bar([i +bar_width for i in index], df.loc['RoW'], bar_width, label='RoW', color='red')

plt.xlabel('Sectors')
plt.ylabel('CO2')
plt.title('CO2 by Sector: EU vs RoW')
plt.xticks([i +bar_width/2 for i in idex], df.columns, rotation=45, ha='right')
plt.legend()





#%%


data_exio.plot_matrix('E', x='Region_to',y='Value', 
                    facet_col='Satellite account', color='Sector_to',
                    base_scenario='baseline',
                    filter_Satellite_account = ['CO2'],
                    path = "Carbon plot",
                    auto_open=True)
        


