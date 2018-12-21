import numpy as np
from src.MemShareSrc import ShareMemWriter
from src.MemShareSrc import ShareMemReader
import os
import time
import pdb



def main():


    cur_dir = "/".join(os.path.dirname(__file__).split("/")[0: -1])
    cur_path = os.path.join(cur_dir, "sharemem.txt")
    print("cur path is ", cur_path)

    x = input()


    if (x == "w"):

        with open(cur_path, "r+", encoding="UTF-8") as fshare:
            print("write data into memory")
            data = np.random.randint(127, size = (352, 288, 3),)
            print("write", data)
            smw = ShareMemWriter(fshare, cur_path, mem_file_size = 1024 * 1024, int_size = 8)
            smw.get_curr_path()
            pdb.set_trace()




            print("start writing --------------------------")
            smw.calibrate()
            tic = time.process_time()
            #smw.write_string()
            smw.write_data_header()
            smw.write_data(data)
            toc = time.process_time()
            #print("time used", 1000*(toc - tic))
            print("writing finished -----------------------")
            input("Press Enter to continue...")

    else:

        with open(cur_path, "r+", encoding="UTF-8") as fshare:
            smr = ShareMemReader(fshare, cur_path, int_size = 8)
            print("start reading --------------------------")
            smr.create_mapping()

            smr.read_data_size()

            while(True):

                tic = time.clock()
                smr.create_mapping()
                smr.copy_buffer()
                smr.read_data_header()
                result = smr.read_data_body()
                toc = time.clock()
                print(np.array(result))
                print("time", 1000*(tic - toc))
                smr.reset()
                smr.close()
                time.sleep(0.2)



if __name__ == "__main__":
    main()