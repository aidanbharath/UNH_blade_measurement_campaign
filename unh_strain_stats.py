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
   
    '''
    print('difference')
    print(s1.max()-s1.min())
    print(s2.max()-s2.min())
    print('standard deviation')
    print(s1.std())
    print(s2.std())
    '''


    start, stop = '2022-11-22 19:05:40', '2022-11-22 20:25:10'

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
   
    for m in range(4):
        d = s2.values[:,m]
        pmx = find_peaks(d,width=50)[0]
        pmn = find_peaks(-d,width=50)[0]

        plist = []
        for i in range(min(pmx.shape[0],pmn.shape[0])):
            if i >= 1:
                plist.append(d[pmx[i]]-d[pmn[i]])

        plist = np.array(plist)
        print('SG', m)
        print('max', plist.max())
        print('mean', plist.mean())
        print('min', plist.min())
        print('std',plist.std())

    return True


if __name__ == "__main__":

    main()
