import numpy as np

from src.MemShareSrc import ShareMemWriter
from src.MemShareSrc import ShareMemReader

#print(ShareMemWriter)
#print(dir(ShareMemWriter))
import os
import time
import pdb

def main():


    cur_dir = "/".join(os.path.dirname(__file__).split("/")[0: -1])
    cur_path = os.path.join(cur_dir, "sharemem.txt")
    #print("cur path is ", cur_path)
    x = raw_input("please type w for write into memory and r for read from memory")


    if (x == "w"):


        data1 = np.random.randint(127, size=(1600, 900, 3))
        #data2 = np.random.randint(127, size=(352, 288, 3))
        #data3 = np.random.randint(127, size=(352, 288, 3))
        #data4 = np.random.randint(127, size=(352, 288, 3))

        smw = ShareMemWriter()
        tic = time.time()
        #smw.write_data([data1, data2, data3 ,data4])
        smw.write_data([data1])
        toc = time.time()
        #print(data1)
        print("time consumed", (toc - tic) * 1000)
        #pdb.set_trace()

    else:

        smr = ShareMemReader()
        while True:
            tic = time.time()
            data = smr.read_data()
            toc = time.time()
            print("time consumed", (toc - tic) * 1000)
            #print(data)
            break

if __name__ == "__main__":
    main()