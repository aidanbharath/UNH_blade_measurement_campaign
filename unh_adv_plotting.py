#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib as mpl

from glob import glob

mpl.rcParams['axes.linewidth'] = 2


font = {
        'family':'monospace',
        'weight':'bold',
        'size':'12'

}

def main():

    ssd = glob('/mnt/*')[0]
    file = f"{ssd}/unh_data/working_files"

    s1 = f"{file}/28175_vLink_strain-2022-11-22.pkl"
    s2 = f"{file}/8145_vLink_strain-2022-11-22.pkl"
    pwr = f"{file}/bow_adv_magnitude-2022-11-22.pkl"

    s1 = pd.read_pickle(s1)
    s2 = pd.read_pickle(s2)
    pwr = pd.read_pickle(pwr)

    pwr = pwr.rolling(10).mean().interpolate()

    start, stop = '2022-11-22 19:35:40', '2022-11-22 19:36:10'

    s1 = s1[start:stop]
    s2 = s2[start:stop]
    pwr = pwr[start:stop]
    
    for df in s1.columns:
        s1[df] = s1[df] - s1[df].mean()

    for df in s2.columns:
        s2[df] = s2[df] - s2[df].mean()

    for df in s1.columns:
        pwr[df] = pwr[df] - pwr[df].mean()

    pwr = pwr.iloc[4:]

    # let us make a simple graph

    fig, ax1 = plt.subplots(figsize=[12,6])
    ax2 = ax1.twinx()
    #l = ax.fill_between(xdata, ydata)
    stime = s1.index
    ptime = pwr.index

    varLabel = 'Inflow Velocity (m/s)'

    label1 = {i:s1.columns[i] for i in range(4)}
    ax1_1, = ax1.plot(stime,s1.values[:,0],label='SG-1',alpha=0.85,linestyle=':')
    ax1_2, = ax1.plot(stime,s1.values[:,1],label='SG-2',alpha=0.85,linestyle=':')
    ax1_3, = ax1.plot(stime,s1.values[:,2],label='SG-3',alpha=0.85,linestyle=':')
    ax1_4, = ax1.plot(stime,s1.values[:,3],label='SG-4',alpha=0.85,linestyle=':')
    ax1_5, = ax1.plot(stime,s2.values[:,0],label='SG-5',alpha=0.85,linestyle=':')
    ax1_6, = ax1.plot(stime,s2.values[:,1],label='SG-6',alpha=0.85,linestyle=':')
    ax1_7, = ax1.plot(stime,s2.values[:,2],label='SG-7',alpha=0.85,linestyle=':')
    ax1_8, = ax1.plot(stime,s2.values[:,3],label='SG-8',alpha=0.85,linestyle=':')

    ax2_1 = ax2.plot(ptime,pwr.values,
                     label=varLabel, 
                     c='k', 
                     linewidth=1.5, 
                     linestyle='-',
                     )

    # set the basic properties
    seconds = mdates.SecondLocator(interval=5)
    ax1.xaxis.set_major_locator(seconds)
    ax1.set_xlabel('Timestamp (UTC)',fontdict=font)
    ax1.set_ylabel(r'Microstrain ($\mu$s)',fontdict=font)
    ax2.set_ylabel(varLabel,fontdict=font)

    #ax1.tick_params(axis='both',grid_linewidth=1,color='k')

    #ax2.set_yticks(np.linspace(ax2.get_yticks()[0],ax2.get_yticks()[-1],len(ax1.get_yticks())))

    ax1ticks = np.arange(-70,80,10)
    ax1.set_yticks(ax1ticks)
    nticks = ax1ticks.shape[0]
    ax2.yaxis.set_major_locator(ticker.LinearLocator(nticks))

    # set the grid on
    ax1.grid(color='k',ls=':')
    
    fig.autofmt_xdate()
    ax1.legend(shadow=True,ncols=4,loc='upper left')
    ax2.legend(shadow=True,ncols=4)
    plt.tight_layout()
    plt.show()

    return True


if __name__ == "__main__":

    main()
