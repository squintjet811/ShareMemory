import ctypes
from Util import ByteIntStringConversion

class MemShareBasic(ByteIntStringConversion):

    def __init__(self):

        def __init__(self, mode=1):
            self.fshareid = None  # memory map file handle
            self.mmap_path = None  # memory map path
            # pull mode
            self.mode = mode
            self.mmap_size = 20
            self.data_size = 0

            self.mm_handle = None  # mmap handle
            self.int_size = 0  # int size

        def read_wbyte(self):
            self.mm_handle.seek(1 + self.int_size * 2)

            val = self.mm_handle.read(1)

            int_val = self.decode_byte(val)
            print("read from wbyte ----------------")

            # print("read from wbyte : ", int_val)
            print("read from wbyte : ", val)

            return int_val

        def read_rbyte(self):
            self.mm_handle.seek(2 + self.int_size * 2)

            val = self.mm_handle.read(1)

            int_val = self.decode_byte(val)

            print("read from rbyte : ", int_val)

            print("read from rbyte : ", val)

            return int_val

        def read_ndbyte(self):
            self.mm_handle.seek(3 + self.int_size * 2)

            val = self.mm_handle.read(1)

            int_val = self.decode_byte(val)

            print("read from ndbyte : ", int_val)

            return int_val

        def write_wbyte(self, val):
            self.mm_handle.seek(1 + self.int_size * 2)
            val_byte = self.uint_2_byte(val)
            self.mm_handle.write(val_byte)

        def write_rbyte(self, val):
            self.mm_handle.seek(2 + self.int_size * 2)
            val_byte = self.uint_2_byte(val)
            self.mm_handle.write(val_byte)

        def write_ndbyte(self, val):
            self.mm_handle.seek(3 + self.int_size * 2)
            val_byte = self.uint_2_byte(val)
            self.mm_handle.write(val_byte)

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
            # print("top dir is", top_dir)
            # print("dir name", data_file_path)


def main():

    msb = MemShareBasic()


if __name__ == "__main__":
    main()
