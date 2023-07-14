import os
import sys
import re

import nptdms as nt

from glob import glob 

def create_dataframe(dname):
    
    ssd = glob('/mnt/*')
    Dir = f"{ssd[0]}/unh_data"
    if not os.path.isdir(Dir):
        print("save directory does not exist")
        sys.exit()

    fnames = []
    for y in glob(F"{dname}/*"):
        for m in glob(f"{y}/*"):   
            fnames.append(glob(f"{m}/*"))
    
    fnames = sorted([f for fn in fnames for f in fn])
    for fname in fnames:
        for f in glob(f"{fname}/*"):

            try:
                if ".done" in f:
                    print('done')
                    continue

                df = nt.TdmsFile(f).as_dataframe()

                drs = f.split('/')
                if not os.path.isdir(f"{Dir}/{drs[2]}"):
                    os.mkdir(f"{Dir}/{drs[2]}")

                pkfile = re.sub(".tdms",".pkl",drs[-1])
                sfn = f"{Dir}/{drs[2]}/{pkfile}"
                if os.path.isfile(sfn):
                    os.remove(sfn)
                

                df.to_pickle(sfn) #change to df.to_csv(sfn) if you want a csv

            except ValueError as e:
                print(f)
                print(e)


    return True
    


def main(dname, *args, **kwds):

    files = [g for g in glob(f"../data/*") if '.tdms' not in g] 
    create_dataframe([f for f in files if dname in f][0])
    return True


if __name__ == "__main__":

    dname = 'YostIMU'
    args, kwds = [], {}
    main(dname, *args, **kwds)
