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

    @staticmethod
    def num_bytes(num):
        bit_length = num.bit_length()
        byte_length = bit_length/8
        if byte_length % 8 != 0: 
            bit_length += 1
        return byte_length

class Encoder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        self.values_list, self.max_int = self.create_list()
        print("Read following values and created encoder:")
        print(self.values_list)
    
    def create_list(self):
        """Open non-encoded binary file and adds integer elements to list 
        
        Returns:
        list: list with signed integer elements that are stored in file in binary form
        int: largest byte size of a number in list
        """

        file_path = self.file_name

        #get total number of list elements (each integer is four bytes large and first byte holds metadata)
        totalElements = (self.file_size - 1)/4

        #make sure list elements are stored properly in file
        remainder = (self.file_size-1) % 4
        if remainder: 
            raise Exception("Elements not correctly stored in binary file")

        #open file and get bytes stored    
        with open(file_path, 'rb') as f:
            self.bytes = f.read()
        
        #iterate through bytes
        current_byte = 1
        values = []
        max_int_size = 0
        while current_byte < totalElements:
            current_block = self.bytes[current_byte:current_byte+4]
            current_byte += 4
            current_block_int = int.from_bytes(current_block, "little", signed=True)
            values.append(current_block_int)
            max_int_size = max(BitTools.num_bytes(current_block_int), max_int_size)
        
        return values, max_int_size

    def encode_values(self):
        print("Encoding Values")
        encoded_bytes = bytes(0)
        encoded_bytes += self.create_first_byte()

        list_index = 0
        while list_index < len(self.values_list):
            block_bit_mask = ""
            non_zero_bytes = bytes(0)
            for i in range(8):
                try:
                    element = self.values_list[list_index]
                    block_bit_mask = "0" if element == 0 else "1"
                    if element != 0:
                        non_zero_bytes += int(element).to_bytes(self.max_int, "little", signed=True)
                    list_index += 1
                except IndexError:
                    break
            encoded_bytes += block_bit_mask
            encoded_bytes += non_zero_bytes
        
        with open(self.file_name, 'wb') as f:
            f.write(encoded_bytes)
                


    
    def create_first_byte(self):
        binary_string = "1" #left most bit signifies encoded

        #values will be encoded in chunks of 8, last chunk may have less than 8 so first byte specifies this
        last_values = len(self.values_list) % 8 
        binary_string += f'{last_values:03b}'

        #number of bytes stored
        binary_string += f'{self.max_int:03b}'
        
        #end with a 0
        binary_string += "0"

        binary_string_as_int = int(binary_string, 2)
        return binary_string_as_int.to_bytes(1, "little")
    
    



class Decoder:
    def __init__(self, file_name):
        self.file_name = file_name
        first_byte_int = 0

        #open file and get collection of bytes
        with open(self.file_name, 'rb') as f: 
            self.encoded_bytes = f.read()

        first_byte = self.encoded_bytes[0]
        first_byte_int = int.from_bytes(first_byte, "little")
            

        #get metadata
        self.int_size = (first_byte_int << 4) >> 1
        self.last_values = (first_byte_int << 1) >> 5
        self.file_size = os.path.getsize(self.file_name)

        #get list of values
        self.values = self.get_values()

        print("Decoding encoded file")
    
    def get_values(self):
        values = [] #store values in array
        byte_number = 1 #keep track of location in byte string 
        int_s = self.int_size

        #handle bytes up until last bit mask
        while byte_number < (self.file_size - self.last_values * self.int_size - 1):
            bit_mask = "{0:08b}".format(self.encoded_bytes[byte_number])
            byte_number += 1

            for bit in bit_mask:
                if bit == "0":
                    values.append(0)
                else:
                    current_val = int.from_bytes(self.encoded_bytes[byte_number:byte_number+int_s], "little", signed=True)
                    values.append(current_val)
                    byte_number += int_s
        
        #handle remainders
        bit_mask = "{0:08b}".format(self.encoded_bytes[byte_number])
        for bit_number in range(self.last_values):
            bit = bit_mask[bit_number]
            if bit == "0":
                values.append(0)
            else:
                current_val = int.from_bytes(self.encoded_bytes[byte_number:byte_number+int_s], "little", signed=True)
                values.append(current_val)
                byte_number += int_s
        
        print("Retrieved following values from encoded file: " + self.values)
    

    def decode(self):
        pass

                


if __name__ == "__main__":
    file_name = sys.argv[1]
    bit_mask = bytes()
    non_zero_values = []

    #open file and get data
    with open(file_name, 'rb') as file:
        first_byte = file.read(1)
        first_byte_int = int.from_bytes(first_byte, "little")
        encoded = BitTools.get_bit(first_byte_int, 7)
    
    if encoded:
        file_decoder = Decoder(file_name)
    else:
        file_encoder = Encoder(file_name)
