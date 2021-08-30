# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 20:13:08 2021

@author: felipe
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shutil
#%% Directory to save results

print('Exporting results--> ...')

if os.path.isdir('./results/'+scen):
    #os.rmdir('./results/'+scen)
    shutil.rmtree('./results/'+scen)
    os.makedirs('./results/'+scen)
else: os.makedirs('./results/'+scen)
#%% Export data and see results
generation_list = list()
imports_list = list()
for year in years:
    for genco, fuel in unit_fuel:
        for period in periods:
            fuel_name = fuel
            generation_list.append([genco, period, year,fuel_name,round(generation[genco,period,year].x,2)])

for year in years: 
    for period in periods:
        imports_list.append(['imports', period,year,'imports',round(imports[period,year].x,2)])

#gen_tech_list = list()
#for year in years:
#    for genco, tech in unit_tech:
#        for period in periods:
#            tech_name = tech
#            gen_tech_list.append([genco, period,year,tech_name,round(generation[genco,period,year].x,2)])
          


results_import = pd.DataFrame(imports_list, columns = ['Unit', 'period', 'year', 'Fuel' ,'Dispatch'])
results_gen = pd.DataFrame(generation_list, columns = ['Unit', 'period', 'year', 'Fuel' ,'Dispatch'])
#results_gen_tech = pd.DataFrame(gen_tech_list, columns = ['Unit', 'period', 'year', 'Tech' ,'Dispatch'])

frames = [results_gen,results_import]
result = pd.concat(frames)
#if save_csv: result.to_excel('./results/'+scen+'/generation.xlsx', sheet_name='generation', index=False) 
results_gen=result


#%%
gen_tmp = results_gen[['Fuel','period','year','Dispatch']]
gen_fuel = gen_tmp.groupby(['year','period','Fuel']).sum()
gen_by_fuel = pd.DataFrame(gen_fuel)
gen_by_fuel=gen_by_fuel.reset_index()
#if save_csv: gen_by_fuel.to_excel('./results/'+scen+'/gen_by_fuel_long_MWh.xlsx', sheet_name='generation_fuel_tech', index=False) 
####
gen_by_fuel['Dispatch']=gen_by_fuel['Dispatch']
gen = gen_by_fuel.pivot_table(index = ['year','period'], columns = 'Fuel', values = 'Dispatch')
if save_csv: gen.to_excel('./results/'+scen+'/gen_by_fuel_wide_GWh.xlsx', sheet_name='generation_wide', index=True) 

#%%
#Plots
col_name = list(gen.columns)
gen = gen[col_name]
#col_name = ['Coal','Diesel','Oil','Gas','LPG','Biomass','Nuclear','Hydro','imports', 'Wind', 'Solar']

pal = sns.color_palette("muted")
gen = gen.reset_index()
gen = gen.set_index('period')
gen_daily = gen.groupby(gen.index // 24)[col_name].sum()
data_perc = gen.divide(gen.sum(axis=1), axis=0)
gen_pie = gen_by_fuel.groupby(by = 'Fuel').sum()
#lgd = plt.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1),labels=None)
#%%
inv_add = list()
for year in years:
    for inv in nondisp_units:
        #print('There were {:.2f} MW of {} added in year {}'.format(cap_inv[inv,year].x, inv, year))
        inv_add.append([year, inv,round(cap_inv[inv, year].x,2)])
    
inv_add_df = pd.DataFrame(inv_add, columns = ['Year','Unit', 'Investment'])
inv_add_df = pd.pivot_table(inv_add_df, values='Investment', index=['Unit'],columns=['Year'], aggfunc=np.sum)
if res_inv:
    plt.figure()
    inv_add_df.plot(kind='bar',stacked =True)
    plt.ylabel('Additional capacity (MW)')
    plt.title('Total Capacity Investment in RES')
    plt.savefig('./results/'+scen+'/cap_inv.png', bbox_inches='tight')
    plt.show()
    

#%%
sort_data = merged.sort_values(by = 'var_cost')
sort_data=sort_data[(sort_data['period']==1)|(sort_data['period']==100)]
sort_data['Cum_cap']=sort_data['cap_mw'].cumsum()
groups = sort_data.groupby("fuel_type")
for name, group in groups:
    plt.plot(group["Cum_cap"], group["var_cost"], marker="o", linestyle="", label=name,)
    plt.legend()
    plt.ylabel('USD/MWh')
    plt.xlabel('MW')
    plt.title('Supply curve')
lgd = plt.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1),labels=None)
plt.savefig('./results/'+scen+'/supply_curve.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
#%%
ceep_total   = 0 
demand_total = 0
ceep_list    = list()
for year in years:
    for period in periods:
        ceep_total   = ceep_total + ceep[period,year].x
        demand_total = demand_total + demand['Industry',period,year]  + demand['Buildings',period,year] + demand['Transport',period,year] + demand['Power',period,year] 
        ceep_list.append([year, period,round(ceep[period,year].x,2),round(demand['Industry',period,year]  + demand['Buildings',period,year] + demand['Transport',period,year] + demand['Power',period,year] ,2)])
ceep_df = pd.DataFrame(ceep_list, columns = ['Year', 'Period', 'CEEP','Demand'])
ceep_df = ceep_df.set_index('Year')
ceep_df.groupby(ceep_df.index)['CEEP'].sum()

ceep_year = ceep_df.groupby('Year').sum()
ceep_year['%-CEEP'] = round(ceep_year['CEEP']/ceep_year['Demand']*100,2)
#%%
storage_total = list()
for year in years:
    for hdam in hydro_storage_units:
        for period in periods:
            storage_total.append([hdam,period,year,storage_level[hdam,period,year].x])
storage_total_df = pd.DataFrame(storage_total, columns = ["unit", 'period','year', 'storage'])
storage_total_df = storage_total_df.pivot_table(index = ['year','period'], columns = 'unit', values = 'storage')
if save_csv: storage_total_df.to_excel('./results/'+scen+'/StorageLevel_Hydro.xlsx', sheet_name='HydroStorageLevel', index=True) 
storage_total_df2 = storage_total_df.reset_index()
#storage_total_df2 = storage_total_df2.set_index()
storage_total_df2 = storage_total_df2.drop(['year','period'], axis='columns')


plt.figure()
plt.stackplot(storage_total_df2.index,storage_total_df2.T/1000, labels=storage_total_df2.columns)
lgd =plt.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1))
plt.title('Hydro storage level')
plt.ylabel('GWh')
plt.xlabel('Period')
plt.savefig('./results/'+scen+'/hydro_storage_level.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

#%%
spillage_total = list()
for hdam in hdam_units:
    for period in periods:
        for year in years:
            spillage_total.append([hdam,period,year,sto_out_flow[hdam,period,year].x])
for hdam in hphs_units:
    for period in periods:
        for year in years:
            spillage_total.append([hdam,period,year,sto_out_flow[hdam,period,year].x])
spillage_total_df = pd.DataFrame(spillage_total, columns = ["unit", 'period','year', 'storage'])
spillage_total_df = spillage_total_df.pivot_table(index = ['year','period'], columns = 'unit', values = 'storage')
if save_csv: spillage_total_df.to_excel('./results/'+scen+'/spillage_hydro_storage.xlsx', sheet_name='Spill_HydroStorage', index=True) 

spillage_total_df2 = spillage_total_df.reset_index()
#spillage_total_df2 = spillage_total_df2.set_index('period')
spillage_total_df2 = spillage_total_df2.drop(['year','period'], axis='columns')
plt.figure()
plt.stackplot(spillage_total_df2.index,spillage_total_df2.T, labels=spillage_total_df2.columns)
plt.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1))
plt.title('Spillage from Hydro (hdam and hphs) units')
plt.ylabel('MWh')
plt.xlabel('Period')
plt.savefig('./results/'+scen+'/spillage_hydro_storage.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

#inflows=inflows.reset_index()
inflows2 = inflows
inflows2 = inflows2.drop(['year','period'], axis='columns')
plt.figure()
plt.plot(inflows2[inflows2.columns])
plt.legend(inflows2.columns,bbox_to_anchor=(1, 1))
plt.ylabel('Inflows (Scaled inflows)')
plt.title('INFLOWS')
plt.savefig('./results/'+scen+'/hydro_inflows.png', bbox_extra_artists=(lgd,), bbox_inches='tight')




#%%
#storage_percet = list()
#for hdam in hdam_units:
#    for period in periods:
#        for year in years:
#            storage_percet.append([hdam,period,year,storage_level[hdam,period,year].x/hdam_max_storage[hdam]])
#for hdam in hphs_units:
#    for period in periods:
#        for year in years:
#            storage_percet.append([hdam,period,year,storage_level[hdam,period,year].x/hphs_max_storage[hdam]])
#storage_percet_df = pd.DataFrame(storage_percet, columns = ["unit", 'period','year', 'storage'])
#storage_percet_df = storage_percet_df.pivot_table(index = ['period','year'], columns = 'unit', values = 'storage')
#if save_csv: storage_percet_df.to_excel('./results/'+scen+'/storage_percet.xlsx', sheet_name='new_sheet_name', index=False) 

#plt.figure()
#plt.plot(storage_percet_df[storage_percet_df.columns])
#plt.legend(storage_percet_df.columns,bbox_to_anchor=(1, 1))
#%% RES TO POWER - HEAT - EV BATTERY
ResToHeat_l  = list()
ResToEV_l    = list()
ResToStat_Sto_l    = list()
ResToStat_Sto_out_l = list()
Heat_res_gen_ind = list()
Heat_res_gen_dh = list()

total_res_to_heat = 0

for year in years:
    for period in periods:
        ResToHeat_l.append([period,year, round(ResToHeat[period,year].x,2)])
        ResToEV_l.append([ period,year, round(ev_sto_in[period,year].x,2)])
        for unit in Stat_storage_unit:
            ResToStat_Sto_l.append([period,year,unit, round(stat_sto_in[unit,period, year].x,2)])
            ResToStat_Sto_out_l.append([period,year,unit, round(stat_sto_out[unit,period, year].x,2)])


for year in years:
    for period in periods:
        for genco in HeatPump_units:
            Heat_res_gen_ind.append([year, period,genco, round(heat_pump_out[genco,period, year].x,2)])
            for chp_market in chp_units:
                Heat_res_gen_dh.append([year, period,chp_market,genco, round(heat_pump_dh[genco,chp_market,period, year].x,2)])

ResToHeat_df = pd.DataFrame(ResToHeat_l, columns = [ 'period','year', 'ResToHeat'])
ResToHeat_df = ResToHeat_df.set_index(['year','period'])
ResToEV_df = pd.DataFrame(ResToEV_l, columns = ['period','year', 'ResToEV'])
ResToEV_df = ResToEV_df.set_index(['year','period'])
ResToStat_Sto_df = pd.DataFrame(ResToStat_Sto_l, columns = ['period','year','unit', 'ResToStaSTO'])
ResToStat_Sto_df = ResToStat_Sto_df.groupby(['year','period']).sum()
ResToStat_Sto_out_df = pd.DataFrame(ResToStat_Sto_out_l, columns = ['period','year','unit', 'StaSTO_Out'])
ResToStat_Sto_out_df = ResToStat_Sto_out_df.groupby(['year','period']).sum()

#ResToStat_Sto_df = ResToStat_Sto_df.set_index(['year','period'])

PowerTo_Sto_Heat_EV = ResToHeat_df.merge(ResToEV_df,left_index=(True), right_index=(True))
PowerTo_Sto_Heat_EV = PowerTo_Sto_Heat_EV.merge(ResToStat_Sto_df,left_index=(True), right_index=(True))
PowerTo_Sto_Heat_EV = PowerTo_Sto_Heat_EV.merge(ResToStat_Sto_out_df,left_index=(True), right_index=(True))

Heat_res_gen_ind_df = pd.DataFrame(Heat_res_gen_ind, columns = ['year','period','HeatPump', 'ResHeat'])
Heat_res_gen_ind_df = Heat_res_gen_ind_df.set_index(['year','period'])
Heat_res_gen_ind_df = Heat_res_gen_ind_df.pivot_table(index = ['year','period'], columns = 'HeatPump', values = 'ResHeat')
Heat_res_gen_ind_df['Total_HP_ind']=Heat_res_gen_ind_df.sum(axis =1)
Heat_res_gen_dh_df = pd.DataFrame(Heat_res_gen_dh, columns = ['year','period','DistrictHeating','HeatPump', 'ResHeat'])
Heat_res_gen_dh_df_total = Heat_res_gen_dh_df.drop(['DistrictHeating','HeatPump'],axis =1).groupby(['year','period']).sum().rename(columns = {'ResHeat':'Total_HP_dh'})
Heat_res_gen_dh_ind_total = Heat_res_gen_dh_df_total.merge(Heat_res_gen_ind_df,left_index=(True), right_index=(True))

if save_csv: Heat_res_gen_dh_ind_total.to_excel('./results/'+scen+'/Heat_res_gen_dh_ind_total.xlsx', sheet_name='Heat_res_gen_dh_ind_total', index=True) 
if save_csv: Heat_res_gen_dh_df.to_excel('./results/'+scen+'/Heat_res_gen_dh_df.xlsx', sheet_name='Heat_res_gen_dh_df', index=True) 
if save_csv: PowerTo_Sto_Heat_EV.to_excel('./results/'+scen+'/PowerTo_Sto_Heat_EV.xlsx', sheet_name='PowerTo_Sto_Heat_EV', index=True) 

heatpump_ind_cap_inv     = list()
heatpump_dh_cap_inv     = list()
for year in years:
    for genco in HeatPump_units:
        heatpump_ind_cap_inv.append([year,  genco, round(heat_pump_ind_cap[genco, year].x,2)])
        for chp in chp_units:
            heatpump_dh_cap_inv.append([year, genco,chp, round(heat_pump_dh_cap[genco,chp,year].x,2)])

HeatPump_ind_inv_df = pd.DataFrame(heatpump_ind_cap_inv, columns = ['year', 'HeatPump','Cap_inv'])
HeatPump_ind_inv_df['Market'] = 'Individual'
HeatPump_ind_inv_df = HeatPump_ind_inv_df.pivot_table(index = ['year', 'Market'], columns = 'HeatPump', values = 'Cap_inv')

HeatPump_dh_inv_df = pd.DataFrame(heatpump_dh_cap_inv, columns = ['year', 'HeatPump','Market','Cap_inv'])
HeatPump_dh_inv_df = HeatPump_dh_inv_df.pivot_table(index = ['year', 'Market'], columns = 'HeatPump', values = 'Cap_inv')

HeatPump_dh_inv_df=HeatPump_dh_inv_df.reset_index()
HeatPump_ind_inv_df=HeatPump_ind_inv_df.reset_index()
HeatPump_inv = pd.concat([HeatPump_dh_inv_df,HeatPump_ind_inv_df]).groupby(['year','Market']).sum()


#%% Traditional boilers
boiler_l      = list()
boiler_dh     = list()
boiler_ind_cap_inv     = list()
boiler_dh_cap_inv     = list()

for year in years:
    for period in periods:
        for genco in thermal_units:
            # boiler_total = boiler_total + boiler_generation[genco,period, year].x
            boiler_l.append([year, period, genco, round(boiler_ind_generation[genco,period, year].x,2)])
            for chp_market in chp_units:
                boiler_dh.append([year, period, genco,chp_market, round(boiler_dh_generation[genco,chp_market,period, year].x,2)])  
                    
boiler_ind_df = pd.DataFrame(boiler_l, columns = ['year','period', 'boiler','TraditionalBoilersHeat_ind'])
boiler_ind_df = boiler_ind_df.set_index(['year','period','boiler'])
boiler_ind_df = boiler_ind_df.pivot_table(index = ['year','period'], columns = 'boiler', values = 'TraditionalBoilersHeat_ind')
boiler_ind_df['Total_boiler_ind']=boiler_ind_df.sum(axis =1)

boiler_dh_df  = pd.DataFrame(boiler_dh, columns = ['year','period','boiler', 'DistHeating','TraditionalBoilersHeat_DH'])
boiler_dh_df_total = boiler_dh_df.drop(['DistHeating','boiler'],axis =1).groupby(['year','period']).sum().rename(columns = {'TraditionalBoilersHeat_DH':'Total_boiler_dh'})
boiler_gen_dh_ind_total = boiler_ind_df.merge(boiler_dh_df_total,left_index=(True), right_index=(True))

boiler_gen_dh_ind_total = boiler_gen_dh_ind_total.reset_index()
if save_csv: boiler_gen_dh_ind_total.to_excel('./results/'+scen+'/boiler_gen_dh_ind_total.xlsx', sheet_name='boiler_gen_dh_ind_total', index=True) 
if save_csv: boiler_dh_df.to_excel('./results/'+scen+'/boiler_dh_df.xlsx', sheet_name='boiler_dh_df', index=True) 

Heat_HP_Boilers_total = boiler_gen_dh_ind_total.set_index(['year','period']).merge(Heat_res_gen_dh_ind_total,left_index=(True), right_index=(True))
Heat_HP_Boilers_total=Heat_HP_Boilers_total.reset_index()
if save_csv: Heat_HP_Boilers_total.to_excel('./results/'+scen+'/Heat_HP_Boilers_total.xlsx', sheet_name='Heat_HP_Boilers_total', index=True) 

for year in years:
    for genco in thermal_units:
        boiler_ind_cap_inv.append([year,  genco, round(trad_boiler_ind_cap_inv[genco, year].x,2)])
        for chp in chp_units:
            boiler_dh_cap_inv.append([year, genco,chp, round(trad_boiler_dh_cap_inv[genco,chp,year].x,2)])

boiler_ind_inv_df = pd.DataFrame(boiler_ind_cap_inv, columns = ['year', 'boiler','Cap_inv'])
boiler_ind_inv_df['Market'] = 'Individual'
boiler_ind_inv_df = boiler_ind_inv_df.pivot_table(index = ['year', 'Market'], columns = 'boiler', values = 'Cap_inv')

boiler_dh_inv_df = pd.DataFrame(boiler_dh_cap_inv, columns = ['year', 'boiler','Market','Cap_inv'])
boiler_dh_inv_df = boiler_dh_inv_df.pivot_table(index = ['year', 'Market'], columns = 'boiler', values = 'Cap_inv')

boiler_dh_inv_df=boiler_dh_inv_df.reset_index()
boiler_ind_inv_df=boiler_ind_inv_df.reset_index()
boiler_inv = pd.concat([boiler_ind_inv_df,boiler_dh_inv_df]).groupby(['year','Market']).sum()

#%% CHP  - HEAT GENERATION FROM CHP
heat_gen_list    = list()
total_heat       = 0
total_heat_gen   = 0
for year in years:
    for period in periods:    
        for genco in chp_units:
            total_heat_gen   = total_heat_gen + round(heat_gen[genco,period,year].x,2)
            heat_gen_list.append([genco, period,year,round(heat_gen[genco,period,year].x,2)])
              
heat_gen_list_df = pd.DataFrame(heat_gen_list, columns = ["unit", 'period','year', 'heat'])
heat_CHP = heat_gen_list_df.pivot_table(index = ['year','period'], columns = 'unit', values = 'heat')
heat_CHP['Total_CHP']=heat_CHP.sum(axis =1)
heat_col_name = list(heat_CHP.columns)

Heat_Total = heat_CHP.merge(Heat_HP_Boilers_total.set_index(['year','period']),left_index=(True), right_index=(True))
if save_csv: Heat_Total.to_excel('./results/'+scen+'/Heat_Total.xlsx', sheet_name='Heat_Total', index=True) 

heat_plot=Heat_Total.reset_index().drop('period',axis = 1).groupby('year').sum()
heat_plot=heat_plot[['Total_CHP','Total_boiler_ind','Total_boiler_dh','Total_HP_dh','Total_HP_ind']]
fig, ax = plt.subplots()
ax=heat_plot.plot(kind='bar', stacked= True)
ax.legend(heat_plot.columns,bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('./results/'+scen+'/Heat.png', bbox_inches='tight')
#%%
ev_storage_level = list()
evToPower = list()
evToHeat = list()
for year in years:
    for period in periods:
        ev_storage_level.append([period,year,round(ev_sto_soc[period,year].x,2)])
        evToPower.append([period,year,round(ev_sto_out[period,year].x,2)])
        #evToHeat.append([period,year,round(ev_heat[period,year].x,2)])


ev_storage_level_df = pd.DataFrame(ev_storage_level, columns = ['period','year', 'soc'])
ev_storage_level_df = ev_storage_level_df.set_index(['year','period'])

evToPower_df = pd.DataFrame(evToPower, columns = ['period','year', 'evToPower'])
evToPower_df = evToPower_df.set_index(['year','period'])

ev_df = ev_storage_level_df.merge(ResToEV_df,left_index=(True), right_index=(True))
ev_df = ev_df.merge(evToPower_df,left_index=(True), right_index=(True))
if save_csv: ev_df.to_excel('./results/'+scen+'/ev_df.xlsx', sheet_name='ev_df', index=False) 

ev_df = ev_df.reset_index().drop(['year'], axis =1) 
ev_df = ev_df.reset_index().drop(['period'], axis =1) 
#ev_df=ev_df.set_index('index')

plt.figure()
plt.stackplot(ev_df['index'],ev_df['soc'],ev_df['ResToEV'],ev_df['evToPower'],
              colors =['r', 'c','b'])
plt.legend(['soc','RestoEV','EVToPower'])
plt.show()
#%%

h2_storage = list()
h2_in_out = list()
h2_out = list()
h2        = list()
h2_gen    = list()
h2_sto_inv= list()
h2_elec_inv= list()
P_to_H2    = list()
H2_gen_tech = list()
h2_cum    = 0

for year in years:
    for period in periods:
        P_to_H2.append([year,period,round(power_to_h2[period,year].x,2)])
    
P_to_H2_df = pd.DataFrame(P_to_H2, columns = ['year','period','ResToH2'])
P_to_H2_df=P_to_H2_df.set_index(['year','period'])
P2X = PowerTo_Sto_Heat_EV.merge(P_to_H2_df,left_index=(True), right_index=(True))
if save_csv: P2X.to_excel('./results/'+scen+'/P2X.xlsx', sheet_name='P2X', index=False) 

for year in years:
    for period in periods:
        for unit in Elec_h2_units:
            H2_gen_tech.append([year, period, unit, round(generation_H2[unit, period, year].x,2)])
            
H2_gen_tech_df = pd.DataFrame(H2_gen_tech, columns = ['year','period','Electrolyzer_tech','H2Gen'])
H2_gen_tech_df = H2_gen_tech_df.pivot_table(index  = ['year','period'], columns = 'Electrolyzer_tech', values = 'H2Gen')
H2_gen_tech_df['TotalH2']=H2_gen_tech_df.sum(axis =1)

for year in years:
    for period in periods:
        for unit in H2_storage_unit:
            #h2_storage.append([period,year,unit,round(h2_sto_soc[unit,period,year].x,2)])
            #h2_in_out.append([period,year,unit,power_to_h2[period,year].x,h2_sto_out[unit,period,year].x ])
            h2.append([year,period,unit,round(power_to_h2[period,year].x,2),round(h2_sto_out[unit,period,year].x,2),round(h2_sto_soc[unit,period,year].x,2) ])         

for year in years:
    for unit in H2_storage_unit:
        h2_sto_inv.append([year,unit,round(h2_sto_max_cap[unit,year].x,2)])

h2_sto_inv_df = pd.DataFrame(h2_sto_inv, columns = ['year','unit', 'H2_sto_inv']).set_index('year')  
h2_sto_inv_df = h2_sto_inv_df.pivot_table(index  = ['year'], columns = 'unit', values = 'H2_sto_inv')

        
for year in years:
    for unit in Elec_h2_units:
        h2_elec_inv.append([year,unit,round(h2_electrolysis_max_cap[unit,year].x,2)])
        
h2_elec_inv_df = pd.DataFrame(h2_elec_inv, columns = ['year','unit', 'H2_Elect_inv']).set_index('year')  
h2_elec_inv_df = h2_elec_inv_df.pivot_table(index  = ['year'], columns = 'unit', values = 'H2_Elect_inv')    
            
h2_df = pd.DataFrame(h2, columns = ['year','period','unit', 'PtoH2', 'h2_sto_out', 'h2_soc']) 
h2_df = h2_df.set_index(['year','period'])
h2_df = h2_df.merge(H2_gen_tech_df,left_index=(True), right_index=(True))   
if save_csv: h2_df.to_excel('./results/'+scen+'/h2_gen_df.xlsx', sheet_name='h2', index=True) 
if save_csv: h2_sto_inv_df.to_excel('./results/'+scen+'/h2_sto_inv_df.xlsx', sheet_name='h2_sto_inv_df', index=True) 
if save_csv: h2_elec_inv_df.to_excel('./results/'+scen+'/h2_elec_inv_df.xlsx', sheet_name='h2_elec_inv_df', index=True) 


#%%
FC_inv= list()
FC_gen= list()
for year in years:
    for period in periods:
        for unit in FC_units:
            FC_gen.append([year,period,unit,round(generation_FC[unit,period,year].x,2)])
            
for year in years:
    for unit in FC_units:
        FC_inv.append([year,unit,round(cap_inv_FC[unit,year].x,2)])      
        
FC_gen_df = pd.DataFrame(FC_gen, columns = ['year','period','unit', 'FC_gen']).set_index(['year','period'])    
FC_gen_df = FC_gen_df.pivot_table(index = ['year','period'], columns = 'unit', values = 'FC_gen')

FC_gen = pd.DataFrame(FC_gen, columns = ['year','period','unit', 'FC_gen']).set_index(['year','unit'])
FC_inv = pd.DataFrame(FC_inv, columns = ['year','unit', 'FC_inv']).set_index(['year','unit'])
FC_gen=FC_gen.drop('period',axis = 1).groupby(['year','unit']).sum()
FC_data = FC_gen.merge(FC_inv, left_index=True, right_index=True)
if save_csv: FC_gen_df.to_excel('./results/'+scen+'/FC_gen.xlsx', sheet_name='FC_gen', index=True) 
if save_csv: FC_inv.to_excel('./results/'+scen+'/FC_inv.xlsx', sheet_name='FC_inv', index=True) 
if save_csv: FC_data.to_excel('./results/'+scen+'/FC_data_agg.xlsx', sheet_name='FC_data_agg', index=True) 

#%%

CO2_power= list()
CO2_heat= list()
for year in years:
    CO2_power.append([year,round(CO2_total[year].x,2)])
    CO2_heat.append([year,round(CO2_total_heat[year].x,2)])

CO2_power_df = pd.DataFrame(CO2_power, columns = ['year','CO2_power']).set_index(['year'])
CO2_heat_df  = pd.DataFrame(CO2_heat, columns = ['year','CO2_heat']).set_index(['year'])
CO2_total_df    = CO2_power_df.merge(CO2_heat_df,left_index=(True), right_index=(True))


#%%
Stat_sto_inv= list()
for year in years:
    for unit in Stat_storage_unit:
        Stat_sto_inv.append([year, unit , round(stat_sto_cap_inv[unit, year].x,2)])
Stat_sto_inv_df = pd.DataFrame(Stat_sto_inv, columns = ['year','Stat_sto_unit','Investment']).set_index(['year','Stat_sto_unit'])


#%%
gen_heat_only = heat_plot
#gen_heat_only = gen_heat_only.merge(evToHeat_df*COP, left_index=True, right_index=True)
#gen_heat_only = gen_heat_only.rename(columns = {'HR_SolarPP':'SolarToHeat','HR_WindPP':'WindToHeat'})

#plt.figure()
#plt.stackplot(gen_heat_only.index,gen_heat_only[gen_heat_only.columns].T)
#plt.legend(gen_heat_only.columns,bbox_to_anchor=(1.35, 1))
#plt.ylabel('MWh (heat)')
#plt.title('Heat generation')
#plt.savefig('./results/'+scen+'/Heat_generation_mix.png')
#%%






#%% Data for plots
gen = gen.reset_index()
gen = gen.set_index(['year','period'])
#Power = gen[['Coal', 'Oil', 'Gas',  'Biomass', 'Nuclear',  'Hydro', 'imports']]
#Power = Power.merge(ResToPower_df, left_index=True, right_index=True)
#Power=Power.rename(columns = {'HR_SolarPP':'Solar','HR_WindPP':'Wind'})
gen_heat = gen.merge(gen_heat_only*-1, left_index=True, right_index=True)
#gen_pie=gen_pie.T
#gen_pie2 = gen_pie
#gen_pie = gen_pie[['Coal','Oil','Gas','Biomass','Nuclear','Hydro','imports', 'Wind', 'Solar']].T
#gen_pie2.reset_index().Fuel.sort_values(col_name,inplace=True)


#gen_daily = gen.groupby(Power.index // 24).sum()
#%%

#ResToHeat_df['ResToHeat']   = ResToHeat_df['HR_SolarPP']+ResToHeat_df['HR_WindPP']
#ResToPower_df['ResToPower'] = ResToPower_df['HR_SolarPP'] +ResToPower_df['HR_WindPP']
#ResToEV_df['ResToEV']       = ResToEV_df['HR_SolarPP'] +ResToEV_df['HR_WindPP']

#ResToX = pd.DataFrame(ResToHeat_df['ResToHeat'])
#ResToX = ResToX.merge(ResToPower_df['ResToPower'], left_index=True, right_index=True)
#ResToX = ResToX.merge(ResToEV_df['ResToEV'] , left_index=True, right_index=True)

ResToX2 = P2X.reset_index()
ResToX2 = ResToX2.drop(['year','period'], axis = 'columns')
plt.figure()
plt.stackplot(ResToX2.index,ResToX2[ResToX2.columns].T/1000)
plt.legend(ResToX2.columns,bbox_to_anchor=(1, 1))
plt.ylabel('[GWh]')
plt.title('RES to X')
plt.savefig('./results/'+scen+'/RES_to_X.png')
plt.show()

#%%
table = pd.pivot_table(gen_by_fuel, values='Dispatch', index=['year'],columns=['Fuel'], aggfunc=np.sum)
table['Total']=table.sum(axis = 1)
table['%-RES']=round((table['Wind']+table['Solar']+table['Hydro']+table['Biomass'])/table['Total']*100,2)
table = pd.DataFrame(table['%-RES'])

#heat = gen_heat_only.reset_index().drop('period', axis =1).groupby('year').sum()
#heat['Total'] = heat.sum(axis = 1)
#heat=round(heat/1000,2)
#heat['CHP'] = heat['Total']-heat['ResHeat']
#heat['%-ResHeat'] = round(heat['ResHeat']/heat['Total'],2)*100
#heat['%-CHP'] = round(heat['CHP']/heat['Total'],2)*100
#heatRes = heat[['ResHeat','%-ResHeat']]

h2_df = h2_df.reset_index().drop(['period','unit'], axis = 1).groupby('year').sum()
#h2_sto_max_cap = pd.DataFrame(h2_sto_max_cap, columns = ['unit','year', 'H2_sto_inv'])
#h2_sto_inv = pd.DataFrame(h2_sto_inv, columns = ['year','unit', 'H2_sto_inv']).set_index('year')
#h2_elec_inv = pd.DataFrame(h2_elec_inv, columns = ['year','unit', 'H2_elec_inv']).set_index('year')
#h2_df = h2_df.merge(h2_sto_inv,left_index=True,right_index=True)
#h2_df = h2_df.merge(h2_elec_inv,left_index=True,right_index=True)

print('Done printing and ploting')
######################################################################################################################
######################################################################################################################
print('####################################################################################')
print('###############################*REPORT*#############################################')
print('####################################################################################')
print('____________________________________________________________________________________')
print('*Investment in renewable Energy*')
print(inv_add_df.to_string())
print('____________________________________________________________________________________')
print('*Percentage Energy Mix - RES (solar, wind, biomass, hydro) and CO2*')
#print('RES = {:.2f} % of demand '.format(100*(gen['Wind'].sum()+gen['Solar'].sum()+gen['Biomass'].sum()+gen['Hydro'].sum())/gen_by_fuel['Dispatch'].sum()))
print(table.to_string())
print('')
print('CO2 Emissions')
print(CO2_total_df.to_string())
print('____________________________________________________________________________________')
print('*Critical Excess of Energy Production*')
print('CEEP by year (GWh) ')
for index, row in ceep_year.iterrows():
  print('Year {}: CEEP = {} GWh ({}%).'.format(index,round(row['CEEP']/1000,2), row['%-CEEP']))
print('____________________________________________________________________________________')
print('*Heat Generaiong (GWh)*') 
print(gen_heat_only.to_string()) 
print(' ') 
print('Capacity Investment in boilers') 
print(boiler_inv.to_string()) 
print(' ') 
print('Capacity Investment in HeatPump') 
print(HeatPump_inv.to_string()) 
print('____________________________________________________________________________________')
print('*Hydrogen generation and capacity*')
#for index, row in h2_df.iterrows():
print('')
print('Hydrogen Gen')
print(h2_df.to_string())
print('')
print('H2 storage investment')
print(h2_sto_inv_df.to_string())
print('')
print('H2 electrolizer investment')
print(h2_elec_inv_df.to_string())
print('____________________________________________________________________________________')
print('*Fuel cells generation and capacity*')
print(FC_data.to_string())
print('____________________________________________________________________________________')
print('*Stationary Storage Investment*')
print(Stat_sto_inv_df.to_string())
print('____________________________________________________________________________________')


File_object = open(r'./results/'+scen+'/report.txt',"w")
File_object.write("#################################################################################### \n")
File_object.write("###############################*REPORT*############################################# \n") 
File_object.write("#################################################################################### \n") 
File_object.write("*Investment in renewable Energy* \n") 
File_object.write(str(inv_add_df)+"\n") 
File_object.write("____________________________________________________________________________________\n") 
File_object.write("*Energy Mix - NCRE (solar, wind, biomass, hror) and CO2 Emissions*\n")
File_object.write(str(table)+"\n")  
File_object.write("CO2 Emissions \n") 
File_object.write(str(CO2_total_df)+"\n")  
File_object.write("____________________________________________________________________________________\n") 
File_object.write("*Critical Excess of Energy Production* \n") 
for index, row in ceep_year.iterrows():
    File_object.write(str('Year {}: CEEP = {} GWh ({}%).'.format(index,round(row['CEEP']/1000,2), row['%-CEEP'])+"\n"))
#File_object.write(str('Percentage of demand = {:.2f}%'.format(ceep_total/demand_total*100))+"\n") 
File_object.write("____________________________________________________________________________________\n")  
File_object.write("*Heat: CHP, Boilers and HeatPumps* \n") 
File_object.write(str(gen_heat_only.to_string())+"\n")  
File_object.write("Capacity Investment in boilers \n")
File_object.write(str(boiler_inv.to_string())+"\n")  
File_object.write("Capacity Investment in boilers \n")
File_object.write(str(HeatPump_inv.to_string())+"\n") 
#for index, row in heat.iterrows():
#    File_object.write(str('Year {}:'.format(index))+"\n")
#    File_object.write(str('Heat (CHP) Generation = {} GWh ({}%).'.format(round(row['CHP']/1000,2), row['%-CHP']))+"\n")  
#    File_object.write(str('RES to Heat Gen       = {:.2f} GWh ({:.2f}%) '.format(row['ResHeat']/1000, row['%-ResHeat']))+"\n")  
File_object.write("____________________________________________________________________________________\n") 
File_object.write('*Hydrogen generation and capacity*\n')
File_object.write("Hydrogen Gen \n") 
File_object.write(str(h2_df.to_string())+"\n")  
File_object.write("H2 storage investment \n") 
File_object.write(str(h2_sto_inv_df.to_string())+"\n")  
File_object.write("H2 electrolizer investment \n") 
File_object.write(str(h2_elec_inv_df.to_string())+"\n") 
#for index, row in h2_df.iterrows():
#    File_object.write(str('Year {}:'.format(index))+"\n")
#    File_object.write(str('H2 (electrolizer) Generation = {} GWh.'.format(round(row['h2_gen']/1000,2)))+"\n")  
#    File_object.write(str('H2 storage investment        = {} GW.'.format(round(row['H2_sto_inv']/1000,2)))+"\n")  
#    File_object.write(str('H2 electrolizer investment   = {} GW.'.format(round(row['H2_elec_inv']/1000,2)))+"\n") 
File_object.write("____________________________________________________________________________________\n") 
File_object.write('*Fuel cells generation and capacity*\n')
File_object.write(str(FC_data.to_string())+"\n") 

#for index, row in FC_data.iterrows():
#    File_object.write(str('Year {}:'.format(index))+"\n")
#    File_object.write(str('Fuel Cells Generation           = {} GWh.'.format(round(row['FC_gen']/1000,2)))+"\n")  
#    File_object.write(str('Fuel Cell generation investment = {} GW.'.format(round(row['FC_inv']/1000,2)))+"\n")  
File_object.write("____________________________________________________________________________________\n") 
File_object.write('*Stationary Storage Investment*\n')
File_object.write(str(Stat_sto_inv_df.to_string())+"\n") 
File_object.write("____________________________________________________________________________________\n") 
File_object.close() 




###############

