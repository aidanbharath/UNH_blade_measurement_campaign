#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob

def main(*args,**kwds):

    ssd = glob('/mnt/*')
    fname = f"{ssd[0]}/unh_data/8145_Vlink"
    #fname = f"{ssd[0]}/unh_data/28175_Vlink"
    vlinks = sorted([vl for vl in glob(f"{fname}/*") 
                     if '2022_11_22' in vl])

    dff = []
    for vlink in vlinks:
        file = pd.read_pickle(vlink)


        keys = file.keys()

        gpsT, wsdaT, data = keys[0], keys[1], keys[[2,3,4,5]]

        df = pd.DataFrame(file[data].values,index=file[wsdaT].values)

        dff.append(df)

    df = pd.concat(dff)

    tsc = lambda x: dt.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
    time = []
    for i in df.index:
        d = i/1e9
        ns = str(d)
        ns = ns.split('.')
        time.append(f"{tsc(i/1e9)}.{ns[-1]}")

    time = pd.to_datetime(time)

    df = pd.DataFrame(df.values, index=time)

    #df.plot(style=".-")
    #plt.show()

    df.to_pickle(f"{ssd[0]}/unh_data/working_files/8145_vLink_strain-2022-11-22.pkl")
    return True


if __name__ == "__main__":

    args, kwds = [], {}
    main(*args, **kwds)
