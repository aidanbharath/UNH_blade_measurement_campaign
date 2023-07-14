#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob

def main(*args,**kwds):

    ssd = glob('/mnt/*')
    fname = f"{ssd[0]}/unh_data/28175_Vlink"
    vlinks = sorted([vl for vl in glob(f"{fname}/*") 
                     if '2022_11_22' in vl])

    dff = []
    for vlink in vlinks:
        file = pd.read_pickle(vlink)

        keys = file.keys()
        gpsT, wsdaT, compass = keys[0], keys[1], keys[-1]

        df = pd.Series(file[compass].values,index=file[wsdaT].values)

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

    df = pd.Series(360*(df.values-df.min())/(df.max()-df.min()), index=time)

    print(360-df.max()/df.min())
    df.plot(style=".-")
    plt.show()

    #df.to_pickle(f"{ssd[0]}/unh_data/working_files/compass_vLink-2022-11-22.pkl")

    return True


if __name__ == "__main__":

    args, kwds = [], {}
    main(*args, **kwds)
