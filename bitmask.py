import csv
import sys
import os


class BitTools:
    @staticmethod
    def get_bit(byte_chunk, bit_number):
        return byte_chunk >> bit_number
    
    @staticmethod
    def set_bit(byte_chunk, bit_number):
        return byte_chunk | (1 << bit_number)

    @staticmethod
    def unset_bit(byte_chunk, bit_number):
        return byte_chunk &(~(1 << bit_number))

class Encoder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        self.values_list = create_list()
        print("Encoding decoded file")
    
    def create_list(self):
        """Open non-encoded binary 
        """
        file_path = self.file_name
        with open(file_path, 'rb') as f:
            #get total number of list elements
            totalElements = (self.file_size - 1)/4

            #make sure list elements are stored properly in file
            remainder = (self.file_size-1) % 4
            if remainder: 
                raise Exception("Elements not correctly stored in binary file")
            
            #iterate through bytes and add them to list 
            byte_index = 2
            

class Decoder:
    def __init__(self, file_name):
        self.file_name = file_name
        print("Decoding encoded file")

if __name__ == "__main__":
    file_name = sys.argv[1]
    bit_mask = bytes()
    non_zero_values = []

    #open file and get data
    with open(file_name, 'rb') as file:
        first_byte = file.read(1)
        first_byte_int = int.from_bytes(first_byte, "big")
        encoded = BitTools.get_bit(first_byte_int, 7)
    
    if encoded:
        Decoder(file_name)
    else:
        Encoder(file_name)
