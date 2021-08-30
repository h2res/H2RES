# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:50:35 2021

@author: felipe
"""

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as GridSpec
#import numpy as np

pal = sns.color_palette("muted")
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.', '//')
explode = (0.2,0.1,0.2,0.1,0.2,0.1,0.2,0.1,0.2)

pal2 = ['dimgray', 'black','black', 'lightskyblue','yellowgreen','red', 'royalblue','brown','darkorange','seagreen','seagreen']
pal_sankey = ['dimgray', 'black', 'lightskyblue','yellowgreen','red', 'royalblue','brown','yellow','darkgreen']
if NoResToHeatInv: pal_heat = ['steelblue', 'deepskyblue', 'lightskyblue']
else: pal_heat = ['yellow','orange','steelblue', 'deepskyblue', 'lightskyblue', 'purple']
col_name = ['Coal','Diesel','Oil','Gas','Biomass','Nuclear','Hydro','imports', 'Wind','Solar']
col_name22 = ['Coal','Diesel','Oil','Gas','LPG','Biomass','Nuclear','Hydro','imports', 'Wind', 'Solar']

gen = gen.reset_index()
#gen_heat_only = gen_heat_only.reset_index()
#gen_heat_only = gen_heat_only.drop('year', axis = 'columns')
#gen_heat_only = gen_heat_only.drop('period', axis = 'columns')

if resolution == 'hour':
    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec.GridSpec(nrows=2, ncols=2, figure=fig)

    ax0 = fig.add_subplot(gs[0, :])
    ax0.stackplot(gen.index,gen[col_name].T, colors=pal2,alpha = 0.8, labels=col_name)
    ax0.set(xlabel='Period', ylabel='[MWh]',title='Electricity generation (demand)')
    ax0.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1),labels=None, prop={'size': 12})
    ax0.plot(df_demand[demand_sectors].sum(axis=1), color='purple',alpha = 0.3)
        
    #ax1 = fig.add_subplot(gs[1, 0])
    #ax1.stackplot(gen_heat_only.index,gen_heat_only[gen_heat_only.columns].T, colors=pal_heat, labels=gen_heat_only.columns,alpha = 0.4)
    #ax1.axhline(y=0, color='black', linestyle='-')
    #ax1.set(xlabel='Period', ylabel='[MWh]',title='Heat generation - All Sources')
    #ax1.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1),labels=None, prop={'size': 12})
    
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.stackplot(gen_daily.index,gen_daily[col_name].T, colors=pal2, labels=col_name,alpha = 0.8)
    ax3.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1),labels=None, prop={'size': 12})
    ax3.set(xlabel='day', ylabel='[MWh]',title='Electricity Generation - Daily scale')

    ax2 = fig.add_subplot(gs[1, 1])
    ax2.pie(gen_pie.Dispatch, autopct='%1.1f%%',startangle=90, labels=gen_pie.index,
            colors=pal2, explode=explode, textprops={'fontsize': 16})
    lgd = plt.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 0.8),labels=None, prop={'size': 16})
    
    plt.tight_layout()
    plt.savefig('./results/'+scen+'/combined.png', bbox_extra_artists=(lgd,), bbox_inches='tight')

    
if resolution == 'daily':
    fig = plt.figure(figsize=(20, 10))
    gs = GridSpec.GridSpec(ncols=2, nrows=2, figure=fig)

    
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.stackplot(gen.index,gen[col_name].T, colors=pal2,alpha = 1, labels=col_name)
    ax0.set(xlabel='Period', ylabel='[MWh]',title='Electricity generation (demand)')
    ax0.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 0.8),labels=None, prop={'size': 12})
    #ax0.plot(df_demand['demand_GWh'], color='red')
        
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.stackplot(gen_heat_only.index,gen_heat_only[gen_heat_only.columns].T, colors=pal_heat, labels=gen_heat_only.columns)
    ax1.axhline(y=0, color='black', linestyle='-')
    ax1.set(xlabel='Period', ylabel='[MWh]',title='Heat generation - All Sources')
    ax1.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 0.8),labels=None, prop={'size': 12})

    ax2 = fig.add_subplot(gs[:, 1])
    ax2.pie(gen_pie.Dispatch, autopct='%1.1f%%',startangle=90, labels=gen_pie.index,
            colors=pal2, explode=explode, textprops={'fontsize': 16})
    lgd = plt.legend(loc=2, fontsize='large',bbox_to_anchor=(1, 0.8),labels=None, prop={'size': 16})
    plt.tight_layout()
    plt.savefig('./results/'+scen+'/combined.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    
    


pie2=gen_by_fuel.groupby(by = ['year','Fuel']).sum()
pie2=pie2.drop('period', axis = 1)
pie3=pie2.unstack().T.reset_index().drop('level_0',axis =1)
pie3.set_index('Fuel').T[col_name].plot(kind='bar', stacked=True,alpha = 0.8, color=pal2)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.title('Generation by fuel and year', color='black')
plt.savefig('./results/'+scen+'/bar_year.png', bbox_inches='tight')

gen.reset_index().drop('index',axis =1).drop('period',axis =1).groupby('year').sum().T.plot(kind='bar',stacked = False)
plt.title('Generation by fuel and year', color='black')
plt.savefig('./results/'+scen+'/bar_year_gen.png', bbox_inches='tight')
