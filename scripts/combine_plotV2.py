import matplotlib.pyplot as plt

pal2 = ['black', 'dimgray','silver', 'lightskyblue', 'blue','yellowgreen','red', 'royalblue','brown','darkorange','seagreen']
col_name22 = ['Coal','Diesel','Oil','Gas','LPG','Biomass','Nuclear','Hydro','imports', 'Wind', 'Solar']
col_name = ['Coal','Diesel','Oil','Gas','Biomass','Nuclear','Hydro','imports', 'Wind','Solar']

gen = gen.reset_index()
fig, axs = plt.subplots(len(gen['year'].unique()), sharex=False,figsize=(8,10))
#fig.suptitle('Generation by year - fuel ')
for i in range(len(gen['year'].unique())):
    data_plot = gen[gen['year']==years[i]]
    data_plot2 = pd.DataFrame(columns = col_name22)
    data_plot2 = data_plot2.append(data_plot).fillna(0)
    data_demand = pd.DataFrame(df_demand[df_demand['year']==years[i]])
    data_demand['total'] = data_demand[demand_sectors].sum(axis=1)
    data_demand=data_demand.set_index('period')
    axs[i].stackplot(data_plot2.period,data_plot2[col_name22].T, colors=pal2,alpha = 0.8, labels=col_name22)
    #axs[i].legend(loc=2, fontsize='large',bbox_to_anchor=(1, 1),labels=None, prop={'size': 12})
    axs[i].set_title(years[i])
    axs[i].set(xlabel='Period', ylabel='[MWh]')
    axs[i].plot(data_demand['total'], color='purple',alpha = 0.2)
    handles, labels = axs[i].get_legend_handles_labels()

fig.legend(handles, labels, loc='right', fontsize='large',bbox_to_anchor=(1.2, 0.4),labels=None, prop={'size': 12})
plt.subplots_adjust(left=0,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.85, 
                    wspace=1, 
                    hspace=0.45)
plt.tight_layout()
plt.show()

