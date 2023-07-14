#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib as mpl

from glob import glob
from scipy.signal import find_peaks

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
    pwr = f"{file}/rotor_thrust-2022-11-22.pkl"

    s1 = pd.read_pickle(s1)
    s2 = pd.read_pickle(s2)
    pwr = pd.read_pickle(pwr)
    
    print('difference')
    print(s1.max()-s1.min())
    print(s2.max()-s2.min())
    print('standard deviation')
    print(s1.std())
    print(s2.std())



    start, stop = '2022-11-22 19:33:40', '2022-11-22 19:36:10'

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

    fig, ax = plt.subplots(4,2,figsize=[16,7],sharex=True)
    stime = s1.index
    ptime = pwr.index
    

    label1 = {i:s1.columns[i] for i in range(4)}
    ax1_1, = ax[0,0].plot(stime,s1.values[:,0],label='SG-1',alpha=0.85,linestyle='-',c='r')
    ax1_2, = ax[0,1].plot(stime,s1.values[:,1],label='SG-2',alpha=0.85,linestyle='-',c='r')
    ax1_3, = ax[1,0].plot(stime,s1.values[:,2],label='SG-3',alpha=0.85,linestyle='-',c='r')
    ax1_4, = ax[1,1].plot(stime,s1.values[:,3],label='SG-4',alpha=0.85,linestyle='-',c='r')
    ax1_5, = ax[2,0].plot(stime,s2.values[:,0],label='SG-5',alpha=0.85,linestyle='-',c='r')
    ax1_6, = ax[2,1].plot(stime,s2.values[:,1],label='SG-6',alpha=0.85,linestyle='-',c='r')
    ax1_7, = ax[3,0].plot(stime,s2.values[:,2],label='SG-7',alpha=0.85,linestyle='-',c='r')
    ax1_8, = ax[3,1].plot(stime,s2.values[:,3],label='SG-8',alpha=0.85,linestyle='-',c='r')

    # set the basic properties
    seconds = mdates.SecondLocator(interval=15)
    for a in ax.flat:
        a.xaxis.set_major_locator(seconds)
        #a.set_xlabel('Timestamp (UTC)',fontdict=font)
        #a.set_ylabel(r'Microstrain ($\mu$s)',fontdict=font)

        ax1ticks = np.arange(-70,80,30)
        a.set_yticks(ax1ticks)

        # set the grid on
        a.grid(color='k',ls=':')
        a.legend(shadow=True,ncols=4,loc='lower left')


    fig.autofmt_xdate()
    #plt.tight_layout()
    plt.subplots_adjust(hspace=0.15,wspace=0.075)
    fig.text(0.5, 0.1, 'Timestamp (UTC)', ha='center' ,fontdict=font)
    fig.text(0.08, 0.5, r'Microstrain ($\mu$s)', va='center',rotation='vertical',fontdict=font)
    plt.show()

    return True


if __name__ == "__main__":

    main()
