from utils.bittools import BitTools
import csv
import os 

class FileReader:
    @staticmethod
    def get_list(file_name):
        funcs_dict = {
            "csv": FileReader.list_from_csv,
            "encoded": FileReader.list_from_encoded,
            "decoded": FileReader.list_from_decoded
        }

        #Check file type and call appropriate function
        file_type = FileReader.get_file_type(file_name)
        if file_type == None: 
            return None #Invalid File Type
        else: 
            return funcs_dict[file_type](file_name)

    
    @staticmethod
    def get_file_type(file_name):
        file_ext = file_name[-3:]

        #Case 1: CSV
        if file_ext == "csv":
            return "csv"
        
        #Case 2: Binary File
        if file_ext == "bin":
            with open(file_name, 'rb') as f:
                file_bytes = f.read()
                first_byte = file_bytes[0]
                encoded = BitTools.get_bit(first_byte, 7)
        
            if encoded: 
                return "encoded"
            else:
                return "decoded"
        
        #Case 3: None of the Above
        return None

    @staticmethod
    def list_from_encoded(file_name):
        values = [] #store values in list
        byte_number = 0 #track byte_number in file
        file_size = os.path.getsize(file_name)
        
        #get metadata from first byte of file 
    
        with open(file_name, 'rb') as f:
            encoded_bytes = f.read()
            first_byte = encoded_bytes[0]
            int_s = (first_byte >> 1) & int("00000111", 2)
            last_values = (first_byte >> 4) & int("00000111", 2)
            byte_number += 1
        
        #handle bytes up until last bit mask
        while byte_number < (file_size - last_values * int_s - 1):
            bit_mask = "{0:08b}".format(encoded_bytes[byte_number])
            byte_number += 1

            for bit in bit_mask:
                if bit == "0":
                    values.append(0)
                else:
                    current_val = int.from_bytes(encoded_bytes[byte_number:byte_number+int_s], "little", signed=True)
                    values.append(current_val)
                    byte_number += int_s
        
        #handle remainders
        if byte_number < file_size:
            #get mask
            bit_mask = "{0:08b}".format(encoded_bytes[byte_number])
            byte_number += 1

            #iterate through mask get and get values
            for bit_number in range(last_values):
                bit = bit_mask[bit_number]
                if bit == "0":
                    values.append(0)
                else:
                    current_val = int.from_bytes(encoded_bytes[byte_number:byte_number+int_s], "little", signed=True)
                    values.append(current_val)
                    byte_number += int_s

        return values
    
    @staticmethod
    def list_from_decoded(file_name):
        values, max = FileReader.list_size_from_decoded(file_name)
        return values


    @staticmethod
    def list_size_from_decoded(file_name):
        file_path = file_name
        file_size = os.path.getsize(file_name)

        #make sure file is correctly stored
        remainder = (file_size - 1) % 4
        if remainder:
            raise Exception("Elements not correctly stored in binary file")
        
        #open file and get bytes stored
        with open(file_path, 'rb') as f:
            decoded_bytes = f.read()
        
        #iterate through bytes and get numbers and max integer size
        current_byte = 1
        values = []
        max_int_size = 0

        while current_byte < file_size:
            #get four bytes and convert to integer
            current_block = decoded_bytes[current_byte:current_byte+4] 
            current_byte += 4
            current_integer = int.from_bytes(current_block, "little", signed=True)

            #add current value to list
            values.append(current_integer)

            #get size of current integer and use it to set max integer size
            curr_integer_size = BitTools.num_bytes(current_integer)
            max_int_size = max(curr_integer_size, max_int_size)
        
        return values, max_int_size


    @staticmethod
    def list_from_csv(file_name):
        values = []
        with open(file_name, 'r') as f:
            f_reader = csv.reader(f, delimiter=",")
            read_values = list(f_reader)[0]
            for val in read_values:
                values.append(int(val))
        
        return values
    
class FileConverter:
    @staticmethod
    def csv_to_binary_file(file_name):
        #get data from file
        values = FileReader.list_from_csv(file_name)

        bytes_string = bytes(1)
        for value in values:
            bytes_string += int.to_bytes(value, 4, "little", signed=True)

        #Write bytes string to file 
        new_file_name = file_name[:-4] + ".bin"
        with open(new_file_name, 'wb') as f:
            f.write(bytes_string)

        return new_file_name




        
    
    
