"""
Created on Fri Jan  8 11:01:48 2021
@author: Felipe Feijoo
"""
#import os
#os.chdir('D:/Dropbox/PUCV/UZagreb/Research/Python_spyder/UCP_montly')
import pandas as pd
#import itertools
import math
import numpy
import sys


#%%
###############################################################################
###############################GENCO DATA and demand data######################
###############################################################################
print('Reading data --> In process')

df                = pd.read_csv(genco_dat)
fuel_cost         = pd.read_csv(fuel_price_dat)
df_demand         = pd.read_csv(demand_dat)
#aval_factor       = pd.read_csv(avl_factor_dat)
aval_factor_plant = pd.read_csv(avl_factor_plant_dat)
inflows           = pd.read_csv(inflows_dat)
import_capacity   = pd.read_csv(import_export)
heat_demand_df    = pd.read_csv(heat_demand_dat)
#ev_storage_df     = pd.read_csv(ev_storage_dat)
ev_transpload_df  = pd.read_csv(ev_transpload_dat)
stat_storage_df   = pd.read_csv(stat_storage_dat) #stationary storage
h2_demand_df      = pd.read_csv(h2_demand_dat)
flex_tech_df      = pd.read_excel(flex_tech_dat, sheet_name='flex_tech')
thermal_tech_df   = pd.read_excel(flex_tech_dat, sheet_name='thermal_tech')
flex_tech_costs_df   = pd.read_excel(flex_tech_dat, sheet_name='tech_cost_years') 
flex_tech_COP_df   = pd.read_excel(flex_tech_dat, sheet_name='COP_HP') 
flex_tech_dh_cap   = pd.read_excel(flex_tech_dat, sheet_name='DistricHeating') 

##############################################################################
fuel_cost['scale'] = (1+0.01)**(fuel_cost['year']-2020)
fuel_unique        = list(fuel_cost.columns)
fuel_unique.remove('scale')
fuel_unique.remove('year')
fuel_unique.remove('period')
fuel_cost2=fuel_cost[fuel_unique].multiply(fuel_cost["scale"], axis="index")
fuel_cost.update(fuel_cost2)
##############################################################################

###############################################################################
################################GENERAL SETS###################################
###############################################################################
#print('Reading data')
units            = list(df['unit_name'])
fuel             = list(df['fuel_type'].unique())
fuel2            = list(df['fuel2'])
technology       = list(df['technology'])
heat_district    = list(heat_demand_df.columns[1:])
fossil_units     = list(df[(df['fuel_type']=='Coal')| (df['fuel_type']=='Gas')|(df['fuel_type']=='Nuclear')|(df['fuel_type']=='Diesel')|(df['fuel_type']=='Oil')|(df['fuel_type']=='Biomass')]['unit_name'])
disp_units       = list(df[(df['technology']=='ICEN')| (df['technology']=='STUR')| (df['technology']=='HDAM')|(df['technology']=='COMC')|(df['technology']=='GTUR')|(df['technology']=='HPHS')]['unit_name'])
hydro_units      = list(df[(df['fuel_type']=='Hydro')]['unit_name'])
biomass_units    = list(df[(df['fuel_type']=='Biomass')]['unit_name'])
hydro_storage_units = list(df[(df['technology']=='HDAM')|(df['technology']=='HPHS')]['unit_name'])
hror_units       = list(df[(df['technology']=='HROR')]['unit_name'])
hdam_units       = list(df[(df['technology']=='HDAM')]['unit_name'])
hphs_units       = list(df[(df['technology']=='HPHS')]['unit_name'])
ncre_units       = list(df[(df['fuel_type']=='Solar') | (df['fuel_type']=='Wind') | (df['fuel_type']=='Biomass') | (df['technology']=='HROR')]['unit_name'])
Bio_Hror_units   = list(df[(df['fuel_type']=='Biomass') | (df['technology']=='HROR')]['unit_name'])
nondisp_units    = list(df[(df['fuel_type']=='Solar') | (df['fuel_type']=='Wind')]['unit_name'])
wind_units       = list(df[(df['fuel_type']=='Wind')]['unit_name'])
solar_units       = list(df[(df['fuel_type']=='Solar')]['unit_name'])


periods          = list(df_demand['period'].unique())
years            = list(df_demand['year'].unique())
n_periods        = len(periods)
#disp_fuels       = ['Coal','Gas','Nuclear','Diesel','Oil','Biomass','Hydro']
#nondisp_fuels    = ['Solar','Wind']

################################################################################################################################################################################################
###################################################################### RESERVE UNITS############################################################################################################
################################################################################################################################################################################################
primary_reserve_units= list(df[(df['PrimaryReserve']=='Y')]['unit_name'])
primary_reserve_wind_units= list(df[(df['PrimaryReserve']=='Y') & (df['fuel_type']=='Wind')]['unit_name'])
primary_reserve_hydropump_units= list(df[(df['PrimaryReserve']=='Y') & (df['technology']=='HDAM')]['unit_name'])
secondary_reserve_units  = list(df[(df['SecondaryReserve']=='Y')]['unit_name'])
reserve_factor    = dict(zip(primary_reserve_units, list(df[(df['PrimaryReserve']=='Y')]['Stab_factor'])))

primary_reserve_FC_units= list(flex_tech_df[(flex_tech_df['PrimaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Fuel cell')]['unit_name'])
primary_reserve_HP_units= list(flex_tech_df[(flex_tech_df['PrimaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Heat pumps')]['unit_name'])
primary_reserve_ELY_units= list(flex_tech_df[(flex_tech_df['PrimaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Electrolizer')]['unit_name'])
primary_reserve_StatStorage_units= list(flex_tech_df[(flex_tech_df['PrimaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name'])
primary_reserve_Desalination_units= list(flex_tech_df[(flex_tech_df['PrimaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Desalination')]['unit_name'])

secondary_reserve_FC_units= list(flex_tech_df[(flex_tech_df['SecondaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Fuel cell')]['unit_name'])
secondary_reserve_HP_units= list(flex_tech_df[(flex_tech_df['SecondaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Heat pumps')]['unit_name'])
secondary_reserve_ELY_units= list(flex_tech_df[(flex_tech_df['SecondaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Electrolizer')]['unit_name'])
secondary_reserve_StatStorage_units= list(flex_tech_df[(flex_tech_df['SecondaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name'])
secondary_reserve_Desalination_units= list(flex_tech_df[(flex_tech_df['SecondaryReserve']=='Y') & (flex_tech_df['Tech_type']=='Desalination')]['unit_name'])

###############################################################################
#############################Flexibility Options DATA#########################
###############################################################################
FC_units           = list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name'])
HeatPump_units     = list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name'])
Elec_h2_units      = list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['unit_name'])
H2_storage_unit    = list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['unit_name'])
Stat_storage_unit  = list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name'])

FC_eff           = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name']),    list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['efficiency'])))
HP_eff           = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['efficiency'])))
H2_eff           = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['efficiency'])))
Sta_sto_eff      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['efficiency'])))

FC_init_cap      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name']),    list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['cap_mw'])))
HP_init_cap      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['cap_mw'])))
HP_ind_init_cap  = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['cap_mw'])))
H2_init_cap      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['cap_mw'])))
Sta_sto_init_cap = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['cap_mw'])))

FC_max_cap       = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name']),    list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['max_cap'])))
HP_max_cap       = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['max_cap'])))
H2_max_cap       = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['max_cap'])))
Sta_sto_max_cap  = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['max_cap'])))

FC_var_cost      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name']),    list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['var_cost'])))
HP_var_cost      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['var_cost'])))
H2_var_cost      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')]['var_cost'])))
Sta_sto_var_cost = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]['var_cost'])))

H2_sto_init      = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['cap_mw'])))
H2_sto_inv_cost  = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['cap_inv_cost'])))
H2_sto_max_cap   = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')]['max_cap'])))

HP_sto_init    = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']), list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['heat_storage_cap'])))
#FC_sto_init    = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name']),    list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['storage_cap'])))
#HP_sto_init    = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['storage_cap'])))

#FC_sto_inv_cost = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['unit_name']),    list(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')]['storage_inv_cost'])))
#HP_sto_inv_cost = dict(zip(list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['unit_name']),   list(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]['storage_inv_cost'])))

cap_costs_long = flex_tech_costs_df.melt(id_vars = ['year'])
cap_costs_long = cap_costs_long.rename(columns = {'variable':'unit_name'})

Elec_cap_costs = pd.merge(flex_tech_df[(flex_tech_df['Tech_type']=='Electrolizer')],cap_costs_long)
Elec_cap_costs_years    = dict(zip(list(zip(Elec_cap_costs[(Elec_cap_costs['Tech_type']=='Electrolizer')]['unit_name'], Elec_cap_costs['year'])), list(Elec_cap_costs[(Elec_cap_costs['Tech_type']=='Electrolizer')]['value'])))

FC_cap_costs = pd.merge(flex_tech_df[(flex_tech_df['Tech_type']=='Fuel cell')],cap_costs_long)
FC_cap_costs_years    = dict(zip(list(zip(FC_cap_costs[(FC_cap_costs['Tech_type']=='Fuel cell')]['unit_name'], FC_cap_costs['year'])), list(FC_cap_costs[(FC_cap_costs['Tech_type']=='Fuel cell')]['value'])))

HP_cap_costs = pd.merge(flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')],cap_costs_long)
HP_cap_costs_years    = dict(zip(list(zip(HP_cap_costs[(HP_cap_costs['Tech_type']=='Heat pumps')]['unit_name'], HP_cap_costs['year'])), list(HP_cap_costs[(HP_cap_costs['Tech_type']=='Heat pumps')]['value'])))

boiler_cap_costs = pd.merge(thermal_tech_df,cap_costs_long)
boiler_cap_costs_years    = dict(zip(list(zip(boiler_cap_costs['unit_name'], boiler_cap_costs['year'])), list(boiler_cap_costs['value'])))

H2sto_costs = pd.merge(flex_tech_df[(flex_tech_df['Tech_type']=='H2 Storage')],cap_costs_long)
H2sto_costs_years    = dict(zip(list(zip(H2sto_costs[(H2sto_costs['Tech_type']=='H2 Storage')]['unit_name'], H2sto_costs['year'])), list(H2sto_costs[(H2sto_costs['Tech_type']=='H2 Storage')]['value'])))

battery_sto_costs = pd.merge(flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')],cap_costs_long)
battery_costs_years    = dict(zip(list(zip(battery_sto_costs[(battery_sto_costs['Tech_type']=='Stationary Elect Storage')]['unit_name'], battery_sto_costs['year'])), list(battery_sto_costs[(battery_sto_costs['Tech_type']=='Stationary Elect Storage')]['value'])))

#############
flex_tech_COP_df_long=flex_tech_COP_df.melt(id_vars = ['year','period'])
HP_COP_period = dict(zip(list(zip(flex_tech_COP_df_long['variable'], flex_tech_COP_df_long['period'], flex_tech_COP_df_long['year'])), list(flex_tech_COP_df_long['value'])))  
####

flex_tech_dh_cap=pd.melt(flex_tech_dh_cap, id_vars=['unit'])
HP_Boiler_dh_init_cap = dict(zip(list(zip(flex_tech_dh_cap['unit'], flex_tech_dh_cap['variable'])), list(flex_tech_dh_cap['value'])))
####
Boiler_decom_start_old = dict(zip(list(thermal_tech_df['unit_name']),list(thermal_tech_df['decom_start_existing_cap'])))
Boiler_decom_start_new = dict(zip(list(thermal_tech_df['unit_name']),list(thermal_tech_df['decom_start_new'])))
Boiler_life_new        = dict(zip(list(thermal_tech_df['unit_name']),list(thermal_tech_df['life_time'])))
Boiler_final_cap       = dict(zip(list(thermal_tech_df['unit_name']),list(thermal_tech_df['final_life_cap'])))
Boiler_decom_rate  ={}

for index, row in thermal_tech_df.iterrows():
    if row['life_time'] == row['decom_start_new']:
        Boiler_decom_rate.update({row['unit_name']:1})
    else:
        row['DecomRate'] = round(1 - 10**(numpy.log10(row['final_life_cap'])/(row['life_time'] - row['decom_start_new'])),3)
        Boiler_decom_rate.update({row['unit_name']:row['DecomRate']})

####
flex_tech_HP_df    = flex_tech_df[(flex_tech_df['Tech_type']=='Heat pumps')]
HP_decom_start_new = dict(zip(list(flex_tech_HP_df['unit_name']),list(flex_tech_HP_df['decom_start_new'])))
HP_life_new        = dict(zip(list(flex_tech_HP_df['unit_name']),list(flex_tech_HP_df['life_time'])))
HP_final_cap       = dict(zip(list(flex_tech_HP_df['unit_name']),list(flex_tech_HP_df['final_life_cap'])))
HP_decom_rate  ={}

for index, row in flex_tech_HP_df.iterrows():
    if row['life_time'] == row['decom_start_new']:
        HP_decom_rate.update({row['unit_name']:1})
    else:
        row['DecomRate'] = round(1 - 10**(numpy.log10(row['final_life_cap'])/(row['life_time'] - row['decom_start_new'])),3)
        HP_decom_rate.update({row['unit_name']:row['DecomRate']})
#print('Generators technical information--> DONE')

####
flex_tech_Sta_sto_df    = flex_tech_df[(flex_tech_df['Tech_type']=='Stationary Elect Storage')]
#Sta_sto_start_old = dict(zip(list(flex_tech_Sta_sto_df['unit_name']),list(flex_tech_Sta_sto_df['decom_start_existing_cap'])))
Sta_sto_decom_start_new = dict(zip(list(flex_tech_Sta_sto_df['unit_name']),list(flex_tech_Sta_sto_df['decom_start_new'])))
Sta_sto_life_new        = dict(zip(list(flex_tech_Sta_sto_df['unit_name']),list(flex_tech_Sta_sto_df['life_time'])))
Sta_sto_final_cap       = dict(zip(list(flex_tech_Sta_sto_df['unit_name']),list(flex_tech_Sta_sto_df['final_life_cap'])))
Sta_sto_decom_rate  ={}

for index, row in flex_tech_Sta_sto_df.iterrows():
    if row['life_time'] == row['decom_start_new']:
        Sta_sto_decom_rate.update({row['unit_name']:1})
    else:
        row['DecomRate'] = round(1 - 10**(numpy.log10(row['final_life_cap'])/(row['life_time'] - row['decom_start_new'])),3)
        Sta_sto_decom_rate.update({row['unit_name']:row['DecomRate']})
print('Generators technical information--> DONE')



###############################################################################
#############################Set AVAL FACTOR FOR NCRES#########################
###############################################################################
inflows_long = inflows.melt(id_vars = ['year','period'])
inflows_long = inflows_long.rename(columns = {'variable':'unit_name'})
inflows_long = inflows_long.rename(columns = {'value':'inflow'})

#Ava.Factor for HPHS
hphs_inflow      = pd.merge(df[(df['technology']=='HPHS')], inflows_long )
hphs_inflow      = dict(zip(list(zip(list(hphs_inflow['unit_name']),list(hphs_inflow['period']),list(hphs_inflow['year']))),list(hphs_inflow['inflow'])))
hphs_max_storage = dict(zip(list(df[(df['technology']=='HPHS')]['unit_name']),list(df[(df['technology']=='HPHS')]['STOCapacity'])))
hphs_efficiency  = dict(zip(list(df[(df['technology']=='HPHS')]['unit_name']),list(df[(df['technology']=='HPHS')]['efficiency'])))

#Storage and Efficiency for Hydro DAM
hdam_inflow      = pd.merge(df[(df['technology']=='HDAM')], inflows_long )
hdam_inflow      = dict(zip(list(zip(list(hdam_inflow['unit_name']),list(hdam_inflow['period']),list(hdam_inflow['year']))),list(hdam_inflow['inflow'])))
hdam_max_storage = dict(zip(list(df[(df['technology']=='HDAM')]['unit_name']),list(df[(df['technology']=='HDAM')]['STOCapacity'])))
hdam_efficiency  = dict(zip(list(df[(df['technology']=='HDAM')]['unit_name']),list(df[(df['technology']=='HDAM')]['efficiency'])))


#Available factor for PHOT, WindONshore, and HROR
aval_factor_plant_long = aval_factor_plant.melt(id_vars = ['year','period'])
aval_factor_plant_long = aval_factor_plant_long.rename(columns = {'variable':'unit_name'})
merged_plant_factor    = pd.merge(df, aval_factor_plant_long)
merged_plant_factor    = merged_plant_factor.rename(columns = {'value':'aval_factor_plant'})
aval_factor_plant      = dict(zip(list(zip(list(merged_plant_factor['unit_name']),list(merged_plant_factor['period']),list(merged_plant_factor['year']))),list(merged_plant_factor['aval_factor_plant'])))

###############################################################################
####Variable cost calculation for generators with time dependent fuel prices###
###############################################################################

fuel_cost_long     = fuel_cost.melt(id_vars = ['year','period'])
fuel_cost_long     = fuel_cost_long.rename(columns = {'variable':'fuel_type'})
merged             = pd.merge(df, fuel_cost_long,how='left')

if merged[merged['value'].isna()]['unit_name'].empty == False:
    print('the unit "' + merged[merged['value'].isna()]['unit_name'] + '" has no fuel price -> STOP')
    sys.exit()

merged['var_cost'] = merged['cost_no_fuel'] + merged['value']/merged['efficiency']
vcost              = list(merged['var_cost'])
unit_time          = list(zip(list(merged['unit_name']),list(merged['period']),list(merged['year'])))
var_cost           = dict(zip(unit_time,vcost))
print('Variable cost estimates--> DONE')

###############################################################################
########################OTHER GENCO TECHNICAL INFORMATION######################
###############################################################################

unit_fuel      = list(zip(list(df['unit_name']),list(df['fuel_type'])))
unit_tech      = list(zip(list(df['unit_name']),list(df['technology'])))
max_load       = dict(zip(list(df['unit_name']),list(df['cap_mw'])))
min_load       = dict(zip(list(df['unit_name']),list(df['min_load_year'])))
cap_factor     = dict(zip(list(df['unit_name']),list(df['cap_factor'])))
tot_prod_cap   = sum(df['cap_mw']*df['cap_factor'])
cost_startup   = dict(zip(list(df['unit_name']),list(df['st_cost'])))
cost_on        = dict(zip(list(df['unit_name']),list(df['cost_on'])))
cap_inv_cost   = dict(zip(list(df['unit_name']),list(df['cap_inv_cost_USD_MW'])))
ramp_cost      = dict(zip(list(df['unit_name']),list(df['RampingCost'])))
ramp_up_rate   = dict(zip(list(df['unit_name']),list(df['RampUpRate'])))
ramp_down_rate = dict(zip(list(df['unit_name']),list(df['RampDownRate'])))
CO2_factor     = dict(zip(list(df['unit_name']),list(df['CO2Intensity'])))
max_inv_period = dict(zip(list(df['unit_name']),list(df['max_inv_period'])))


decom_start_old = dict(zip(list(df['unit_name']),list(df['decom_start_existing_cap'])))
decom_start_new = dict(zip(list(df['unit_name']),list(df['decom_start_new'])))
life_new        = dict(zip(list(df['unit_name']),list(df['life_time'])))
final_cap       = dict(zip(list(df['unit_name']),list(df['final_life_cap'])))
decom_rate  ={}


for index, row in df.iterrows():
    if row['life_time'] == row['decom_start_new']:
        decom_rate.update({row['unit_name']:1})
    else:
        row['DecomRate'] = round(1 - 10**(numpy.log10(row['final_life_cap'])/(row['life_time'] - row['decom_start_new'])),3)
        decom_rate.update({row['unit_name']:row['DecomRate']})
        if row['life_time'] == row['decom_start_new']:
            print(row['unit_name'])
            
print('Generators technical information--> DONE')

###############################################################################
############################DEMAND and MARKET DATA#############################
###############################################################################
demand_sectors = list(['Industry', 'Buildings', 'Transport','Power'])
demand_long = df_demand.melt(id_vars = ['year','period'])
demand_long = demand_long.rename(columns = {'variable':'demand_sector'})
demand    = dict(zip(list(zip(list(demand_long['demand_sector']),list(demand_long['period']),list(demand_long['year']))),list(demand_long['value'])))

H2_demand_long = h2_demand_df.melt(id_vars = ['year','period'])
H2_demand_long = H2_demand_long.rename(columns = {'variable':'demand_sector'})
H2_demand    = dict(zip(list(zip(list(H2_demand_long['demand_sector']),list(H2_demand_long['period']),list(H2_demand_long['year']))),list(H2_demand_long['value'])))

import_ntc   = dict(zip(list(import_capacity['period']),list(import_capacity['Import_capacity'])))
exports      = dict(zip(list(import_capacity['period']),list(import_capacity['total_exports'])))


###############################################################################
############################Other PARAMENTERS#############################
###############################################################################
rps            = dict(zip(years,rps))
NPV            = dict(zip(years,NPV))
CO2_limit      = dict(zip(years,CO2_limit))
Thermal_Decom_ind  = dict(zip(years,ThermalDecomInd))
HP_Decom_ind  = dict(zip(years,HeatPumpDecomInd))
StaSto_Decom_ind= dict(zip(years,StaStoDecomInd))


TechChange_solar= dict(zip(years,TechChangeSolar))
TechChange_wind = dict(zip(years,TechChangeWind))

solar_tech_change = list()
for unit in solar_units:
    for year in TechChange_solar.keys():
        solar_tech_change.append([unit, year,TechChange_solar.get(year)])
        
wind_tech_change = list()
for unit in wind_units:
    for year in TechChange_wind.keys():
        wind_tech_change.append([unit, year,TechChange_wind.get(year)])
        
solar_tech_change = pd.DataFrame(solar_tech_change, columns = ['Unit', 'year', 'tech_change'])   
wind_tech_change = pd.DataFrame(wind_tech_change, columns = ['Unit', 'year', 'tech_change']) 
TechChange = pd.concat([solar_tech_change,wind_tech_change], axis=0)

TechChange = dict(zip(list(zip(list(TechChange['Unit']),list(TechChange['year']))),list(TechChange['tech_change']))) 
print('Demand data--> DONE')

###############################################################################
########################HEAT TECHNICAL INFORMATION######################
###############################################################################
chp_units          = list(df[(df['CHPType']=='Y')]['unit_name'])
CHPMaxHeat         = dict(zip(list(df[(df['CHPType']=='Y')]['unit_name']),list(df[(df['CHPType']=='Y')]['CHPMaxHeat'])))
CHPPowerLossFactor = dict(zip(list(df[(df['CHPType']=='Y')]['unit_name']),list(df[(df['CHPType']=='Y')]['CHPPowerLossFactor'])))
CHPPowerToHeat     = dict(zip(list(df[(df['CHPType']=='Y')]['unit_name']),list(df[(df['CHPType']=='Y')]['CHPPowerToHeat'])))
STOSelfDischarge   = dict(zip(list(df[(df['CHPType']=='Y')]['unit_name']),list(df[(df['CHPType']=='Y')]['STOSelfDischarge'])))
STOCapacity_heat   = dict(zip(list(df[(df['CHPType']=='Y')]['unit_name']),list(df[(df['CHPType']=='Y')]['STOCapacity'])))
#heat_demand        = dict(zip(list(heat_demand_df['period']),list(heat_demand_df['heat_demand_total'])))
heat_demand_long=heat_demand_df.melt(id_vars = ['year','period'])
heat_demand_long=heat_demand_long.rename(columns = {'variable':'unit_name'})
heat_demand = dict(zip(list(zip(list(heat_demand_long['unit_name']),list(heat_demand_long['period']),list(heat_demand_long['year']))),list(heat_demand_long['value'])))
print('Generators technical Heating demand and CHP units--> DONE')

###############################################################################
#Variable cost calculation for thermal generators with time dependent fuel prices#
###############################################################################
thermal_units     = list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['unit_name'])
heat_merged       = pd.merge(thermal_tech_df, fuel_cost_long)
heat_vcost        = list(heat_merged['value']/heat_merged['efficiency'])
heat_unit_time    = list(zip(list(heat_merged['unit_name']),list(heat_merged['period']),list(heat_merged['year'])))
heat_var_cost     = dict(zip(heat_unit_time,heat_vcost))

Thermal_init_cap    = dict(zip(list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['unit_name']),
                               list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['cap_mw'])))
Thermal_ind_init_cap = dict(zip(list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['unit_name']),
                               list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['cap_mw'])))

Thermal_cap_inv_cost= dict(zip(list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['unit_name']),
                               list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['cap_inv_cost'])))
Thermal_max_cap     = dict(zip(list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['unit_name']),
                               list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['max_cap'])))
Thermal_CO2         = dict(zip(list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['unit_name']),
                               list(thermal_tech_df[(thermal_tech_df['fuel_type']=='Gas')|(thermal_tech_df['fuel_type']=='Oil')|(thermal_tech_df['fuel_type']=='Biomass')]['CO2Intensity'])))


print('Heat variable cost estimates--> DONE')

###############################################################################
###############################EV Storage INFORMATION######################
###############################################################################
#ev_sto_max_cap = dict(zip(list(zip(list(ev_storage_df['period']),list(ev_storage_df['year']))),list(ev_storage_df['ev_storage'])))
ev_Demand =dict(zip(years,ev_Demand_year))
ev_year_total = ev_transpload_df.groupby(['year'])['ev_transp_load'].sum()
ev_year_total_profile_dict =dict(zip(years,list(ev_year_total)))

ev_norm_fact={x:float(ev_Demand[x])/ev_year_total_profile_dict[x] for x in years}
ev_norm_fact_df = pd.DataFrame(list(ev_norm_fact.items()),columns = ['year','ev_norm_factor'])
ev_transpload_df = pd.merge(ev_transpload_df, ev_norm_fact_df, how="left", on=["year"])
ev_transpload_df['ev_demand_period_year'] =ev_transpload_df['ev_transp_load']*ev_transpload_df['ev_norm_factor']

ev_transp_load = dict(zip(list(zip(list(ev_transpload_df['period']),list(ev_transpload_df['year']))),list(ev_transpload_df['ev_demand_period_year'])))
ev_transp_load_max_year = ev_transpload_df.groupby('year')['ev_demand_period_year'].max()
ev_transp_load_max_year = ev_transp_load_max_year.reset_index().rename(columns={'ev_demand_period_year':'ev_demand_period_year_max'})
#ev_transp_load_max_year.rename(columns={'ev_demand_period_year':'ev_demand_period_year_max'})
ev_transpload_df = pd.merge(ev_transpload_df, ev_transp_load_max_year, how="left", on=["year"])

ev_availability = dict(zip(list(zip(list(ev_transpload_df['period']),list(ev_transpload_df['year']))),list(ev_parked_connected*((1-ev_peak_demand)+ev_peak_demand*(1-ev_transpload_df['ev_demand_period_year']/ev_transpload_df['ev_demand_period_year_max'])))))
#Number of EV connected and ready to V2G

for key1, key2 in ev_availability.keys():
    if  math.isnan(ev_availability[key1, key2]):
        ev_availability[key1, key2] = 0
        
stat_sto_max_cap = dict(zip(list(zip(list(stat_storage_df['period']),list(stat_storage_df['year']))),list(stat_storage_df['stat_storage']))) #stationary storage
print('Reading data --> DONE')
