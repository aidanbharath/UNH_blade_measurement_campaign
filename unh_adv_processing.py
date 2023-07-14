#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from glob import glob


def main():
    
    ssd = glob('/mnt/*')[0]
    file = f"{ssd}/unh_data/working_files/bow_adv-2022-11-22.pkl"
    data = pd.read_pickle(file)

    #wh = np.where(data[['Corr B1','Corr B2','Corr B3']] <= 90)
    #wh = np.where(data[['Corr B1','Corr B2']] <= 90)
    wh = np.where(data[['Corr B1']] <= 85)
    data.iloc[wh[0]] = np.nan
    print(data)

    df = np.where(data['Vel 1/X/E'].diff().abs() > 0.1)[0]

    data[data['Vel 1/X/E'].diff().abs() >= 0.75] = np.nan
    data[data['Vel 2/Y/N'].diff().abs() >= 0.75] = np.nan
    #data[['Vel 1/X/E','Vel 2/Y/N','Vel 3/Z/U']].plot()
    #plt.show()

    magnitude = np.sqrt(data['Vel 1/X/E']**2+data['Vel 2/Y/N']**2+data['Vel 3/Z/U']**2)

    mg = pd.Series(magnitude, index=data.index)

    #mg.plot()
    #plt.show()

    mg.to_pickle(f"{ssd}/unh_data/working_files/bow_adv_magnitude-2022-11-22.pkl")


    return True



if __name__ == "__main__":

    main()
