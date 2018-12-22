import mmap
import numpy as np
import ctypes
import time
import os.path
import os


class ShareMemWriter(object):

    def __init__(self, mem_file_size = 1280 * 1280, mode = 1):

        self.fshareid = None #memory map file handle
        self.mmap_path = None #memory map path
        # pull mode
        self.mode = mode

        self.input_data = None #input data
        self.mm_handle = None #mmap handle

        #data header
        self.int_size = 0 #size of int32 based on system, only updated in writer side
        self.wbyte = 0
        self.rbyte = 0
        self.ndbyte = 0

        #arbitary size
        self.mmap_size = mem_file_size * 8
        self.data_size = 0
        self.mem_file_size = mem_file_size
        self.calibrate_all()

    def calibrate_all(self):

        self.get_curr_path()
        self.calibrate_int_size()
        self.calibrate_memorymappingfile()
        self.create_mapping()


    def calibrate_memorymappingfile(self):

        if self.check_mem_exists() and os.path.getsize(self.mmap_path) >= self.mmap_size:

            print("mem file size satisfied")

        else:

            with open(self.mmap_path, "w+b") as fopen_once:
                content = np.arange(self.mem_file_size).astype(np.double)
                fopen_once.write(content)
            print(self.mmap_path)
            size = os.path.getsize(self.mmap_path)
            print("create file size of ", size)


        self.open_memory_mapping_file()

    def calibrate_int_size(self):

        self.int_size = ctypes.sizeof(ctypes.cast(0, ctypes.POINTER(ctypes.c_int32)))
        print("set int size to : ", self.int_size)

    def open_memory_mapping_file(self):

        self.fshareid = open(self.mmap_path, "r+")

    def get_curr_path(self):

        path_name = os.path.dirname(__file__)
        top_dir = os.path.split(path_name)[0]
        data_file_path = os.path.join(top_dir, "memorymapfile", "memorymap.txt")

        self.mmap_path = data_file_path
        print("top dir is", top_dir)
        print("dir name", data_file_path)

    def check_mem_exists(self):

        result = os.path.isfile(self.mmap_path)

        return result

    def create_mapping(self):

        self.mm_handle = mmap.mmap(self.fshareid.fileno(), access=mmap.ACCESS_WRITE, length=self.mmap_size)

    def write_string(self):
        #for test purpose
        self.mm_handle.write(b"hello world")
        self.mm_handle.flush()


    def read_data_header(self):

        cur_wbyte = int(str(self.mm_handle.read(1)))
        cur_rbyte = int(str(self.mm_handle.read(1)))
        cur_ndbyte = int(str(self.mm_handle.read(1)))


        return 0

    def uint_2_byte(self, data_uint):

        result_buffer = str(data_uint).encode("utf-8")

        return result_buffer

    def int_2_byte(self, data_int):

        result_buffer = ctypes.cast(data_int, ctypes.POINTER(ctypes.c_int32))

        return result_buffer

    #write the data_header
    def write_data_header(self):

        self.reset()


        #print("cur", self.mm_handle.tell())
        #tic = time.time()
        self.mm_handle.write(str(self.int_size).encode("utf-8"))
        #self.mm_handle.write(bytearray(self.int_size))
        #toc = time.time()
        #print("time", (toc - tic) * 1000)
        print("next", self.mm_handle.tell())
        print("cur position", self.mm_handle.tell())
        self.mm_handle.write(self.int_2_byte(self.mmap_size))
        print(ctypes.sizeof(ctypes.cast(self.mmap_size, ctypes.POINTER(ctypes.c_int32))))
        print("next position", self.mm_handle.tell())
        self.mm_handle.write(self.int_2_byte(self.data_size))

        self.mm_handle.write(self.uint_2_byte(self.wbyte))
        self.mm_handle.write(self.uint_2_byte(self.rbyte))
        self.mm_handle.write(self.uint_2_byte(self.ndbyte))

    #convert data based on its type to buffer
    def data_2_buffer(self, data):

        data_type_buffer = self.uint_2_byte(0)
        if type(data).__module__ == np.__name__:
            #for image data it could be compressed to uint8
            if np.issubdtype(data.dtype, np.integer):
                if np.max(data) < 256:
                    print("convert to image data size")
                    buffer_data = data.astype(np.uint8)


                else:
                    buffer_data = data.astype(np.int32)
                    data_type_buffer = self.uint_2_byte(1)

            else:

                buffer_data = data.astype(np.double)
                data_type_buffer = self.uint_2_byte(2)

        else:

            if type(data) is str:

                buffer_data = data
                data_type_buffer = self.uint_2_byte(3)

        print("write data type", data_type_buffer)

        self.mm_handle.write(data_type_buffer)

        #print("size of data", data.shape)
        return buffer_data


    def int_2_buffer(self, data):

        data_buffer = ctypes.cast(data, ctypes.POINTER(ctypes.c_int32))
        return data_buffer




    def write_data(self, data):

        self.write_data_header()
        nsz_array = len(data)
        self.mm_handle.write(self.int_2_buffer(nsz_array))

        print("cur posi: ", self.mm_handle.tell())
        print("data len: ", nsz_array)
        for i in range(nsz_array):

            cur_data = data[i]
            print("cur_data size", cur_data.shape)

            pdim = self.int_2_buffer(len(cur_data.shape)) #write number of dimension
            print("write num of dim", len(cur_data.shape))
            self.mm_handle.write(pdim)

            nsztotal = 1

            for i in range(len(cur_data.shape)):

                nsztotal = nsztotal * cur_data.shape[i]

                pdim_size =self.int_2_buffer(cur_data.shape[i])

                self.mm_handle.write(pdim_size) #write current dimension size


            #write data
            print("cur data type", cur_data.dtype)
            buffer_data = self.data_2_buffer(cur_data).flatten().tobytes()
            print("buffer_data", buffer_data)
            print("before position", self.mm_handle.tell())
            self.mm_handle.write(buffer_data)
            a = self.mm_handle.tell()
            print("after position", a)
            self.mm_handle.seek(a - nsztotal)
            print("size total", nsztotal)
            print("read write data", self.mm_handle.read(nsztotal))

        self.mm_handle.flush()

        return 0

    #reset the starting position of the share memory
    def reset(self):

        self.mm_handle.seek(0)

    #close the handle
    def close(self):

        self.mm_handle.close()



class ShareMemReader(object):

    def __init__(self, mode = 1):

        self.fshareid = None  # memory map file handle
        self.mmap_path = None  # memory map path
        # pull mode
        self.mode = mode
        self.mmap_size = 20
        self.data_size = 0

        self.mm_handle = None  # mmap handle
        self.int_size = 0 # int size

        self.wbyte = 0
        self.rbyte = 0
        self.ndbyte = 0


        self.content = None
        self.content_idx = 0

        self.calibrate()

    def calibrate(self):
        self.get_curr_path()
        self.calibrate_memorymappingfile()
        self.create_mapping()
        self.calibrate_int_size()
        self.read_data_size()
        self.create_mapping() #put the entire space as inside the calibrate

    def calibrate_memorymappingfile(self):

        self.fshareid = open(self.mmap_path, 'r+')

    def calibrate_int_size(self):

        content = self.mm_handle.read(1)
        self.int_size = int(content.decode("utf-8"))
        print("get the target int size ", self.int_size)


    def create_mapping(self):

        self.mm_handle = mmap.mmap(self.fshareid.fileno(), length=self.mmap_size, access=mmap.ACCESS_COPY)

        #self.mm = mmap.mmap(-1, length=, prot=mmap.PROT_WRITE | mmap.PROT_READ)


    def get_curr_path(self):

        path_name = os.path.dirname(__file__)
        top_dir = os.path.split(path_name)[0]
        data_file_path = os.path.join(top_dir, "memorymapfile", "memorymap.txt")

        self.mmap_path = data_file_path
        print("top dir is", top_dir)
        print("dir name", data_file_path)

    def read_data_size(self):

        temp_cont = self.mm_handle.read(self.int_size)
        data_temp_filesz = self.buffer_2_int(temp_cont)
        #print(self.mm.tell())
        self.mmap_size = data_temp_filesz.contents.value
        print("size read from memory file : ", self.mmap_size)
        self.mm_handle.close()
        self.mm_handle = None

        return 0

    def char_2_int(self):

        o_temp = self.buffer_2_int(self.content[self.content_idx:self.content_idx + self.int_size])
        o_value = o_temp.contents.value
        self.content_idx = self.content_idx + self.int_size
        return o_value

    def copy_buffer(self):
        #here the temporarly solution is just to copy the entire buffer
        print("current pos", self.mm_handle.tell())
        #self.seek(4 + self.int_size * 2)
        self.data_size = self.mmap_size - 4  - self.int_size * 2
        print("data size : ", self.data_size)
        self.content = self.mm_handle.read(self.mmap_size - 4  - self.int_size * 2)
        self.content_idx = 0

    def read_data_header(self):

        num_byte_shift = 1 + self.int_size * 2
        self.mm_handle.seek(num_byte_shift)
        self.wbyte = self.decode_byte(self.mm_handle.read(1))
        self.rbyte = self.decode_byte(self.mm_handle.read(1))
        self.ndbyte = self.decode_byte(self.mm_handle.read(1))
        print("finised reading data_header -----------------")


    def buffer_2_int(self, buffer):

        data_int = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_int32))

        return data_int



    def decode_byte(self, my_byte):

        my_string = str(my_byte.decode("utf_8"))
        print("my_string is", my_string)
        my_val = int(my_string)

        return my_val

    def buffer_2_data(self, data_buffer, data_size, data_type):

        if data_type == 0:

            data_retrieved = np.frombuffer(data_buffer, dtype=np.uint8, count = data_size)

        elif data_type == 1:

            data_retrieved = np.frombuffer(data_buffer, dtype=np.int32, count = data_size)

        elif data_type == 2:

            data_retrieved = np.frombuffer(data_buffer, dtype=np.double, count = data_size)

        elif data_type == 3:

            data_retrieved = str(data_buffer.decode("utf-8"))
        print("data retrieved", data_retrieved)
        return data_retrieved

    def read_data(self):

        self.read_data_header()
        self.copy_buffer()

        nsz_array = self.char_2_int() #get the size of array
        print("size of array is :  ", nsz_array)
        data_returned = []
        print("content_idx start", self.content_idx)
        for i in range(nsz_array):

            num_dim = self.char_2_int()
            print("content_idx sz", self.content_idx)
            print("num of dim is ", num_dim)
            data_size = 1
            dim_array = []


            for j in range(num_dim):

                nsz_dim = self.char_2_int()
                print("content_idx dim", self.content_idx)
                data_size = data_size * nsz_dim
                dim_array.append(nsz_dim)
                print("dimen", dim_array)

            data_type = self.decode_byte(self.content[self.content_idx: self.content_idx + 1])  # data type is 1 byte data
            self.content_idx = self.content_idx + 1
            data_buffer = self.content[self.content_idx : self.content_idx + data_size ]
            self.content_idx = self.content_idx + data_size #one byte for datatype, the rest for data
            print("content_idx", self.content_idx)
            print("data type is : ", data_type)
            print("data size is ", data_size)
            print("data_buffer", data_buffer)

            data_flat = self.buffer_2_data(data_buffer, data_size, data_type)

            if data_type is not 3:

                data_reshaped = data_flat.reshape(dim_array)

            else:

                data_reshaped = data_flat

            print("data_reshaped", data_reshaped)
            data_returned.append(data_reshaped)

        return data_returned

    def reset(self):

        self.mm_handle.seek(0)

    def close(self):

        self.mm_handle.close()


