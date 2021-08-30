# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 08:37:00 2021

@author: felipe feijoo
"""
#%%
#MAIN
###############################################################################
######################SENARIO NAME and single parameters#######################
###############################################################################
scen = '90RPS+CO2Limit+CEEP_5pct'
rps_inv        = True    # Options: True / False
carbonLimit    = False    # Options: True / False
res_inv        = True     # Options: True / False
hydro_storage  = True     # Options: True / False
exports_dat    = False    # Options: True / False
save_csv       = True     # Options: True / False
ceep_limit     = True     # Options: True / False
NoResToHeatInv = False    # Options: True / False
PrimaryReserve = True
SecondaryReserve = True
#General Paramenters
resolution       = 'hour'  # Options -> 'hour', 'daily'.
rps              = list([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.9])
NPV              = list([1,0.78,0.61,0.48,0.38,0.3,0.23])   #IR 5%
TechChangeSolar  = list([1, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5])
TechChangeWind   = list([1, 0.95, 0.9, 0.8, 0.7, 0.6, 0.5])
ThermalDecomInd  = list([1, 0.6, 0.3, 0, 0, 0, 0])
HeatPumpDecomInd = list([1, 0.6, 0.3, 0, 0, 0, 0])
StaStoDecomInd   = list([1, 0.6, 0.3, 0, 0, 0, 0])
#TechChangeWind  = list([1, 0.95, 0.95, 0.92, 0.9, 0.88, 0.85])
CO2_limit        = list([4753928*100,4753928*0.8,4753928*0.6,4753928*0.4,4753928*0.3,4753928*0.2,4753928*0.1])
reserve          = 1        # Reserve capacity  = reserve * demand
carbon_price     = 10        # Carbon price in $/tCO2
ceep_parameter   = 0.05     # % of demand used as an upper bound
Import_Price     = 45       # $/MWh
V2G_cost         = 25       # Vehicle to grid cost
#stat_EES_cost   = 25       # stationary electricity energy storage cost

COP             = 3.5
h2_eff          = 0.65      #Electricity to H2 (electrolyzers efficiency) 
FC_eff          = 0.65  
RtoH_var_cost   = 10 

RtoH2_cost      = 120

#### V2G
ev_Grid_P_max   = 10
ev_sto_max      = 100
ev_sto_min      = 0
ev_Grid_eff     = 0.9
ev_peak_demand  = 0     #percentage of cars driving at peak hour
ev_parked_connected = 1   #percentage of cars connected at peak hour
ev_Demand_year   = list([0, 0, 0,0,0,0,0])

###############################################################################
### GENCO/Demand data (enter genco data file name with extension)##############
###############################################################################
#genco_dat             = './data/data_genco_sdewes.csv'
#demand_dat            = './data/demand_2020_2050_sdewes.csv'
#fuel_price_dat        = './data/fuel_cost_USD_MWh_2020_2050_sdewes.csv'
#avl_factor_dat        = './data/ncre_aval_factor.csv'
#avl_factor_plant_dat  = './data/ncre_aval_factor_plant_zones_2020_2050_sdewes.csv'
#inflows_dat           = './data/Scaled_inflows_HR_2020_2050_sdewes.csv' 
#import_export         = './data/import_export_data.csv' 
#heat_demand_dat       = './data/heat_demand_HR_2020_2050_H2storage.csv'
#ev_storage_dat        = './data/ev_storage_2050.csv'
#ev_transpload_dat     = './data/ev_transp_load.csv'
#stat_storage_dat      = './data/stat_storage_2050_sdewes_low.csv'
#h2_demand_dat         = './data/demand_H2_2020_2050_H2Storage.csv'
#flex_tech_dat         = './data/flex_tech_template.xlsx'

genco_dat             = './data/Favignana_genco_kWh_reserves.csv'
demand_dat            = './data/Favignana_demand_kWh_2020_2050csv.csv'
fuel_price_dat        = './data/Favignana_fuel_cost_kWh_2020_2050.csv'
#avl_factor_dat        = './data/ncre_aval_factor.csv'
avl_factor_plant_dat  = './data/Favignana_avalfactor_v2.csv'
inflows_dat           = './data/Scaled_inflows_HR_2020_2050_sdewes.csv' 
import_export         = './data/Favignana_import_export_data.csv' 
heat_demand_dat       = './data/Favignana_heat_demand_2020_2050_kWh.csv'
water_demand_dat       = './data/water_consumption_profile.csv'
ev_storage_dat        = './data/ev_storage_2050.csv'
ev_transpload_dat     = './data/Favignana_ev_transp_load_sbagliato.csv'
stat_storage_dat      = './data/stat_storage_2050_sdewes_low.csv'
h2_demand_dat         = './data/Favignana_H2demand_2020_2050_zero.csv'
flex_tech_dat         = './data/flex_tech_template_reserve.xlsx'
###############################################################################
### GENCO/Demand data (enter genco data file name with extension)##############
###############################################################################
print('Reading and processing data')
exec(open("scripts/read_process_data.py").read())
print('Building and solve the model')
exec(open("scripts/Build_model_ev.py").read())
print('Printing and ploting results')
exec(open("scripts/export_plot_ev.py").read())
#exec(open("scripts/combine_plot.py").read())
exec(open("scripts/combine_plotV2.py").read())
###############################################################################
###############################################################################



