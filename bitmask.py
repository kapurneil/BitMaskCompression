import csv
import sys
import os
from utils.bittools import BitTools


class BinaryUtility:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_ext = file_name[-3:]
        self.values = []
        
        if self.file_ext == "csv":
            self.read_from_csv()

    
    def read_from_csv(self):
        with open(self.file_name, 'r') as f:
            f_reader = csv.reader(f, delimiter=",")
            read_values = list(f_reader)[0]
            for val in read_values:
                self.values.append(int(val))
        print("Read CSV file with following values: ")
        print(self.values)
    
    def csv_to_binary_file(self):
        bytes_string = bytes(1)
        for value in self.values:
            bytes_string += int.to_bytes(value, 4, "little", signed=True)

        #Write bytes string to file 
        new_file_name = self.file_name[:-4] + ".bin"
        with open(new_file_name, 'wb') as f:
            f.write(bytes_string)
        
        print("Created binary file: " + new_file_name)


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
        while current_byte < self.file_size:
            current_block = self.bytes[current_byte:current_byte+4]
            current_byte += 4
            print("Current block " + str(current_block))
            current_block_int = int.from_bytes(current_block, "little", signed=True)

            print("Current Block Int " + str(current_block_int))
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
                    block_bit_mask += "0" if element == 0 else "1"
                    if element != 0:
                        non_zero_bytes += int(element).to_bytes(self.max_int, "little", signed=True)
                    list_index += 1
                except IndexError:
                    remaining_zeros = 8 - i
                    for j in range(remaining_zeros):
                        block_bit_mask += "0"
                    break
            
            #convert bitmask to bytes and add bitmask and list to encoded_bytes
            block_mask_as_bytes = int(block_bit_mask, 2).to_bytes(1, "little")
            encoded_bytes += block_mask_as_bytes
            encoded_bytes += non_zero_bytes
        
        with open(self.file_name, 'wb') as f:
            f.write(encoded_bytes)
                


    
    def create_first_byte(self):
        binary_string = "1" #left most bit signifies encoded

        #values will be encoded in chunks of 8, last chunk may have less than 8 so first byte specifies this
        last_values = len(self.values_list) % 8 
        binary_string += f'{last_values:03b}'

        #number of bytes stored
        print(self.max_int)
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

        first_byte_int = self.encoded_bytes[0]
        print(first_byte_int)
            

        """ get metadata 
        1 bit - valid 
        3 bits - last bit mask size 
        3 bits - size of integer in bytes
        1 bit - trailing zero
        """

        self.int_size = (first_byte_int >> 1) & int("00000111", 2)
        self.last_values = (first_byte_int >> 4) & int("00000111", 2)
        self.file_size = os.path.getsize(self.file_name)

        #get list of values
        self.values = self.get_values()

        print("Decoding encoded file")
    
    def get_values(self):
        values = [] #store values in array
        byte_number = 1 #keep track of location in byte string 
        int_s = self.int_size

        #handle bytes up until last bit mask
        print(self.file_size - self.last_values * self.int_size - 1)
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
        if byte_number < self.file_size:
            bit_mask = "{0:08b}".format(self.encoded_bytes[byte_number])
            print("byte number: ", byte_number)
            print("bit mask: ", bit_mask)
            byte_number += 1
            for bit_number in range(self.last_values):
                bit = bit_mask[bit_number]
                if bit == "0":
                    values.append(0)
                else:
                    current_val = int.from_bytes(self.encoded_bytes[byte_number:byte_number+int_s], "little", signed=True)
                    values.append(current_val)
                    byte_number += int_s
        
        print("Retrieved following values from encoded file: " + str(values))
        return values
    

    def decode_values(self):
        decoded_bytes = bytes(1)
        for element in self.values:
            decoded_bytes += int.to_bytes(element, 4, "little", signed=True)
        
        with open(self.file_name, 'wb') as f:
            f.write(decoded_bytes)


                


if __name__ == "__main__":
    file_name = sys.argv[1]
    file_extension = file_name[-3:]

    if file_extension == "csv":
        binary_converter = BinaryUtility(file_name)
        binary_converter.csv_to_binary_file()
    elif file_extension == "bin":
        bit_mask = bytes()
        non_zero_values = []

        #open file and get data
        with open(file_name, 'rb') as file:
            first_byte = file.read(1)
            first_byte_int = int.from_bytes(first_byte, "little")
            encoded = BitTools.get_bit(first_byte_int, 7)
        
        if encoded:
            file_decoder = Decoder(file_name)
            file_decoder.decode_values()
        else:
            file_encoder = Encoder(file_name)
            file_encoder.encode_values()
    else:
        raise Exception("Invalid file type provided.")


    
