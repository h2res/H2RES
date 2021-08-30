# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:50:35 2021

@author: felipe
"""

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as GridSpec
import numpy as np
import plotnine as p9
from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap



col_name2 = ['year','period','Coal','Diesel','Oil','Gas','Biomass','Nuclear','Hydro','imports', 'Wind', 'Solar']
gen2=gen.reset_index()
gen2=gen2[col_name2]
gen4=pd.melt(gen2, id_vars = ['year','period'], value_vars = col_name)
col_name22 = ['Solar','Wind','imports','Hydro','Nuclear','Biomass','Gas', 'Diesel','Oil', 'Coal']
pal22 = ['seagreen', 'darkorange', 'brown','steelblue','red', 'yellowgreen','lightskyblue','black','black','dimgray']

gen4['Fuel']= gen4['Fuel'].astype('category')
gen4['Fuel']=gen4['Fuel'].cat.reorder_categories(col_name22)
gen4['Fuel'] = pd.Categorical(gen4['Fuel'], categories=col_name22, ordered=True)


plot = (p9.ggplot(gen4, aes('period', 'value', fill='Fuel'))
 + p9.geom_area()
 + p9.scale_fill_manual(values=pal22)
 + p9.ylab('Generation [MWh]')
 + p9.xlab('Periods [hour]')
 + p9.labs(title='Generation by year and fuel/technology')
 + facet_wrap('~year', nrow = 3))

#plot.save(filename = './results/'+scen+'/plotnine_test.png', height=5, width=5, units = 'in', dpi=1000)
p9.ggsave(plot=plot, filename='./results/'+scen+'/Year_generation.png', dpi=1200)

##############################################################################################################
#storage_total_hydro = storage_total_df.reset_index()
#storage_total_hydro =pd.melt(storage_total_hydro, id_vars = ['year','period'], value_vars = hydro_storage_units)

#plot_hydro_storage = (p9.ggplot(storage_total_hydro, aes('period', 'value', fill='unit'))
# + p9.geom_area()
# + p9.scale_fill_manual(values=pal22)
# + p9.ylab('Storage level [MWh]')
# + p9.xlab('Periods [hour]')
# + p9.labs(title='Hydro storage')
# + facet_wrap('~year', nrow = 3)
# + p9.theme(figure_size=(8, 8)))
#p9.ggsave(plot=plot_hydro_storage, filename='./results/'+scen+'/hydro_storage_by_year.png', dpi=1200)