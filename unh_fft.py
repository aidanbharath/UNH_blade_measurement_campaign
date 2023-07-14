#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sc

from scipy.fft import fft, fftfreq
from glob import glob

def fft_window(ds):

    # Number of sample points
    N = ds.shape[0]
    # sample spacing
    T = (ds.index[1]-ds.index[0]).total_seconds()
    x = np.linspace(0.0, N*T, N, endpoint=False)
    y = ds.values
    yf = fft(y)
    
    from scipy.signal import blackman
    w = blackman(N)
    ywf = fft(y*w)
    xf = fftfreq(N, T)[:N//2]
     
    return xf, ywf, N

def main():
    
    ssd = glob('/mnt/*')
    fname = f"{ssd[0]}/unh_data/working_files"
    fnames = sorted(glob(f"{fname}/*"))

    v0 = pd.read_pickle(fnames[0])
    v1 = pd.read_pickle(fnames[1])
    comp = pd.read_pickle(fnames[2])

    v0 = v0[:'2022-11-22 12:25']
    v1 = v1[:'2022-11-22 12:25']
    comp = comp[:'2022-11-22 12:25']

    v0 = v0.iloc[:,3]-v0.iloc[:,3].mean()
    v1 = v1.iloc[:,3]-v1.iloc[:,3].mean()
    comp = comp-comp.mean()
   
    v0x, v0y, N = fft_window(v0)
    v1x, v1y, N = fft_window(v1)
    compx, compy, N = fft_window(comp)

    rmean = 1
    v0m = pd.Series(2.0/N * np.abs(v0y[1:N//2])).rolling(rmean).mean()
    v1m = pd.Series(2.0/N * np.abs(v1y[1:N//2])).rolling(rmean).mean()
    compm = pd.Series(2.0/N * np.abs(compy[1:N//2])).rolling(rmean).mean()

    v0max = v0m.argmax()
    v0ymax = v0y.argmax()
    v1max = v1m.argmax()
    v1ymax = v1y.argmax()
    compmax = compm.argmax()
    compymax = compy.argmax()
    print(v0max,v0ymax)
    print(v1max,v1ymax)
    print(compmax,compymax)

    print(v0x[1:N//2][v0m.argmax()],v0y.max())
    print(v1x[1:N//2][v1m.argmax()],v1y.max())
    print(compx[1:N//2][compm.argmax()],compy.max())

    plt.loglog(v0x[1:N//2], v0m.values, '-b')
    plt.loglog(v1x[1:N//2], v1m.values, '-r')
    plt.loglog(compx[1:N//2], compm.values, '-g')
    plt.legend(['v0', 'v1', 'comp'])
    plt.grid(True, which='both',ls='-')
    plt.show()

    
    # reconstruct timeseries
    v0f = v0x[1:N//2][v0y.argmax()]
    v1f = v1x[1:N//2][v1y.argmax()]
    compf = compx[1:N//2][compy.argmax()]

    print(N,2*np.abs(v0y[v0ymax])/N)
    p = np.pi*2
    v0c = lambda x: 20*(2*np.abs(v0y[v0ymax])/N)*np.cos((p*v0f)*x+np.angle(v0y[v0ymax]))
    v1c = lambda x: np.abs(v1y[v1ymax])*np.cos((p/v1f)*x+np.angle(v1y[v1ymax]))
    compc = lambda x: np.abs(compy[compymax])*np.cos((p/compf)*x+np.angle(compy[compymax]))

    N = v0.shape[0]
    T = (v0.index[1]-v0.index[0]).total_seconds()
    x = np.arange(0,N*T,T)

    plt.plot(x,v0c(x),label='v0 reconstructed')
    plt.plot(x,v0.values,label='v0 raw')
    #plt.plot(x,v1c(x),label='v1')
    #plt.plot(x,compc(x),label='comp')
    plt.legend()
    plt.grid()
    plt.show()

    return True



if __name__ == "__main__":

    main()
