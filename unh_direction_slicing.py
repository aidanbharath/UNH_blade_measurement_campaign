#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob


def main():
    
    ssd = glob('/mnt/*')
    fname = f"{ssd[0]}/unh_data/working_files"
    fnames = sorted(glob(f"{fname}/*"))

    print(fnames)
    v0 = pd.read_pickle(fnames[0])
    v1 = pd.read_pickle(fnames[1])
    comp = pd.read_pickle(fnames[4])
    

    v0 = v0['2022-11-22 19:00':'2022-11-22 20:25']
    v1 = v0['2022-11-22 19:00':'2022-11-22 20:25']
    comp = comp['2022-11-22 19:00':'2022-11-22 20:25']

    ctr = np.arange(5,365,10)
    bnd = [[i-5,i+5] for i in ctr]
    
    grp = {}
    for i, b in enumerate(bnd):
        idx = np.where(np.logical_and(comp>=b[0],comp<b[1]))
        grp[ctr[i]] = idx[0].flatten()

    ax = plt.subplot()
    pValue = v0.iloc[grp[205],2]
    v0.iloc[:,0:3].plot(ax=ax)
    comp.plot(ax=ax,c='k')
    pValue.plot(ax=ax,style='.')
    plt.show()


    return True



if __name__ == "__main__":

    main()
