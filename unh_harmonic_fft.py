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

    v0 = pd.read_pickle(fnames[0])
    v1 = pd.read_pickle(fnames[1])
    comp = pd.read_pickle(fnames[4])

    v0 = v0[:'2022-11-22 20:25']
    v1 = v0[:'2022-11-22 20:25']
    comp = comp[:'2022-11-22 20:25']

    ctr = np.arange(5,365,10)
    bnd = [[i-5,i+5] for i in ctr]
    
    grp = {}
    for i, b in enumerate(bnd):
        idx = np.where(np.logical_and(comp>=b[0],comp<b[1]))
        grp[ctr[i]] = idx[0].flatten()

    np.linspace(0,1,v0.index.shape[0])
    print(v0.iloc[grp[95]])

    N = v0.index.shape[0]
    T = (v0.index[1]-v0.index[0]).total_seconds()
    t = np.array([n*T for n in range(N)])
    s = pd.Series(30*np.sin(2*np.pi*0.003895*t+0.10),index=v0.index)
    ax = plt.subplot()
    pValue = v0.iloc[grp[205],2]-v0.iloc[grp[205],2].mean()
    #v0.iloc[:,0:3].plot(ax=ax)
    #comp.plot(ax=ax,c='k')
    pValue.plot(ax=ax,style='.')
    s.plot(ax=ax,color='r')
    
    plt.show()

    return True



if __name__ == "__main__":

    main()
