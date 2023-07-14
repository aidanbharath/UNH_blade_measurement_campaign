#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

from glob import glob


def main():

    ssd = glob('/mnt/*')[0]
    file = f"{ssd}/unh_data/unh_processed/*"
    fnames = sorted(glob(file))
    vsUnits = fnames[-1]
    vsData = fnames[2]

    units = pd.read_csv(vsUnits)
    data = pd.read_csv(vsData)

    for i in data.columns:
        print(i)

    dt = []
    for idx, r in data.iterrows():
        y, m, d = int(r['Year']), int(r['Month']), int(r['Day'])
        h, M = int(r['Hour']), int(r['Minute'])
        s = f"{r['second']}".split('.')
        ts = f"{y}-{m}-{d} {h}:{M}:{s[0]}.{s[-1]}"
        dt.append(ts)

    time  = pd.to_datetime(dt)

    freq = pd.Series((120/40)*data['Turbine Freq.'].values,index=time)
    pwr = pd.Series((1/10)*data['DumpLoad Power 1sec'].values,index=time)
    freq.plot()
    pwr.plot()
    plt.show()

    #freq.to_pickle(f"{ssd}/unh_data/working_files/rotor_rpm-2022-11-22.pkl")
    #pwr.to_pickle(f"{ssd}/unh_data/working_files/power_kW-2022-11-22.pkl")


if __name__ == "__main__":

    main()
