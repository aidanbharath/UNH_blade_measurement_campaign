#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob
from datetime import timedelta

def main():
    
    ssd = glob('/mnt/*')
    fname = f"{ssd[0]}/unh_data/working_files"
    fnames = sorted(glob(f"{fname}/*"))

    for f in fnames:
        print(f)
    v0 = pd.read_pickle(fnames[0])
    v1 = pd.read_pickle(fnames[1])
    comp = pd.read_pickle(fnames[4])

    v0m = v0[:'2022-11-22 20:25']
    v1 = v1[:'2022-11-22 20:25']
    compm = comp[:'2022-11-22 20:25']

    ctr = np.arange(5,365,10)
    bnd = [[i-5,i+5] for i in ctr]
   
    rng = np.linspace(0.00001,0.001,10)
    for m in rng:
        comp = compm
        v0 =v0m
        idx = v0.index
        iidx = []
        for i, ii in enumerate(idx):
            iidx.append(ii+timedelta(seconds=i*m))

        ct = pd.to_datetime(iidx)
        comp = pd.Series(comp.values,index=ct)
        vidx = v0.index
        comp = comp.reindex(comp.index.union(vidx)).interpolate(method='time').reindex(vidx)

        #v0 = v0[:'2022-11-22 22:25']
        #comp = comp[:'2022-11-22 22:25']

        grp = {}
        for i, b in enumerate(bnd):
            idx = np.where(np.logical_and(comp>=b[0],comp<b[1]))
            grp[ctr[i]] = idx[0].flatten()

        pSTD = v0.iloc[grp[95],0].std()
        print(f"std: {pSTD} ,", f"Dilation: {m}")

        comp = comp/90+24
        ax = plt.subplot()
        pValue = v0.iloc[grp[95],0]
        v0.iloc[:,0].plot(ax=ax)
        comp.plot(ax=ax,c='k')
        pValue.plot(ax=ax,style='.')
        plt.show()
   

    return True



if __name__ == "__main__":

    main()
