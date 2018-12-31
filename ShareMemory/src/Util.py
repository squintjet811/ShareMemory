from abc import ABCMeta, abstractmethod
import ctypes

class ByteIntStringConversion:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self):

        return "1.0"

    @abstractmethod
    #convert single int value to string
    def encode_byte(self, data_uint):

        result_buffer = str(data_uint).encode("utf-8")

        return result_buffer

    @abstractmethod
    def decode_byte(self, my_byte):

        my_string = str(my_byte.decode("utf_8"))
        print("my_string is", my_string)
        my_val = int(my_string)

        return my_val

    @abstractmethod
    def buffer_2_int(self, buffer):

        data_byte = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_int32))
        data_int = data_byte.contents.value

        print("data_byte", data_byte)

        return data_int

    @abstractmethod
    def int_2_byte(self, data_int):

        result_buffer = ctypes.cast(data_int, ctypes.POINTER(ctypes.c_int32))

        return result_buffer

    @abstractmethod
    def int_2_buffer(self, data):

        data_buffer = ctypes.cast(data, ctypes.POINTER(ctypes.c_int32))

        return data_buffer


