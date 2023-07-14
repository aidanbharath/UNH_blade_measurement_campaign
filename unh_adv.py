#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pandas as pd
import matplotlib.pyplot as plt

from glob import glob


def main():

    ssd = glob('/mnt/*')[0]
    file = f"{ssd}/unh_data/unh_processed/*"
    fnames = sorted(glob(file))
    vsUnits = fnames[3]
    vsData = fnames[4]

    units = pd.read_csv(vsUnits)
    data = pd.read_csv(vsData)

    print(data[data.columns[6:]])
    for i in data.columns:
        print(i)

    dt = []
    for idx, r in data.iterrows():
        y, m, d = int(r['YYYY']), int(r['MM']), int(r['dd'])
        h, M = int(r['HH']), int(r['mm'])
        s = f"{'{:0.9f}'.format(r['ss.sss'])}".split('.')
        ts = f"{y}-{m}-{d} {h}:{M}:{s[0]}.{s[-1]}"
        dt.append(ts)

    time  = pd.to_datetime(dt)

    data = pd.DataFrame(data[data.columns[6:]].values,index=time,columns=data.columns[6:])
    print(data)
    '''
    u = pd.Series(data['Vel 1/X/E'].values,index=time)
    v = pd.Series(data['Vel 2/Y/N'].values,index=time)
    w = pd.Series(data['Vel 3/Z/U'].values,index=time)
    c1 = pd.Series(data['Corr B1'].values,index=time)
    c2 = pd.Series(data['Corr B2'].values,index=time)
    c3 = pd.Series(data['Corr B3'].values,index=time)
    #pwr = pd.Series((1/10)*data['DumpLoad Power 1sec'].values,index=time)
    ax = plt.subplot()
    c1.plot(ax=ax)
    c2.plot(ax=ax)
    c3.plot(ax=ax)
    #pwr.plot()
    plt.show()
    '''
    data.to_pickle(f"{ssd}/unh_data/working_files/bow_adv-2022-11-22.pkl")
    #pwr.to_pickle(f"{ssd}/unh_data/working_files/power_kW-2022-11-22.pkl")


if __name__ == "__main__":

    main()
