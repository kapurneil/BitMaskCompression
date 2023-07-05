from utils.bittools import BitTools
from utils.typetools import DataHelper
import csv
import os
import struct 

class FileReader:
    @staticmethod
    def get_list(file_name: str):
        """
        From a file containing a list of integers, determines file type, and then reads
        and returns list of integers.

        Parameters:
        file_name (str): file that will be read

        Returns:
        list: list of integers read from file or None if invalid file
        """

        #appropriate function based on file type
        funcs_dict = {
            "csv": FileReader.list_from_csv,
            "encoded": FileReader.list_from_encoded,
            "decoded": FileReader.list_from_decoded
        }

        #Check file type
        file_type = FileReader.get_file_type(file_name)

        #Call appropriate function based on file type
        if file_type == None: 
            return None #Invalid File Type
        else: 
            return funcs_dict[file_type](file_name)

    
    @staticmethod
    def get_file_type(file_name: str):
        """
        From a provided file name, returns one of the following file types:
        -CSV file
        -Bit mask encoded binary file
        -Bit mask decoded binary file

        Parameters:
        file_name (str): The name of the file 

        Returns:
        str: 'csv' if .csv file or 'encoded' or 'decoded' for a .bin file

        """

        #get file extension from file
        file_ext = file_name[-3:]

        #Case 1: CSV
        if file_ext == "csv":
            return "csv"
        
        #Case 2: Binary File
        if file_ext == "bin":
            #open file and check first bit to see if encoded or decoded
            with open(file_name, 'rb') as f:
                file_bytes = f.read()
                first_byte = file_bytes[0]

                #get first bit of file
                encoded = BitTools.get_bit(first_byte, 7)
            
            #1 means encoded while 0 means decoded
            if encoded: 
                return "encoded"
            else:
                return "decoded"
        
        #Case 3: None of the Above
        return None

    @staticmethod
    def list_from_encoded(file_name: str):
        """
        From a bitmask encoded .bin file, extracts stored numbers and returns a list with values

        Parameters
        file_name (str): encoded .bin file with numerical values in binary form

        Returns
        list: list with numbers found in bitmask encoded binary file 

        """

        values = [] #store values in list
        byte_number = 0 #track byte_number in file
        file_size = os.path.getsize(file_name)
        
        #get metadata
        is_encoded, is_float, last_values, num_size, chr_rep = FileReader.metadata_from_binary(file_name)
        byte_number += 1

        #if not encoded raise error
        if not is_encoded:
            raise Exception("File provided is not a bit mask encoded binary file")

        #get bytes from file
        with open(file_name, 'rb') as f:
            encoded_bytes = f.read()
    
        
        #handle bytes up until last bit mask
        while byte_number < (file_size - last_values * num_size - 1):
            #gets bit mask at location
            bit_mask = "{0:08b}".format(encoded_bytes[byte_number])
            byte_number += 1

            #iterate through bit mask and populate array
            for bit in bit_mask:
                if bit == "0":
                    if is_float:
                        values.append(0.0)
                    else:
                        values.append(0)
                else:
                    current_val = struct.unpack(chr_rep, encoded_bytes[byte_number:byte_number+num_size])[0]
                    values.append(current_val)
                    byte_number += num_size
        
        #handle remainders if list length is not divisible by 8
        if byte_number < file_size:
            #get mask
            bit_mask = "{0:08b}".format(encoded_bytes[byte_number])
            byte_number += 1

            #iterate through mask get and get values
            for bit_number in range(last_values):
                bit = bit_mask[bit_number]
                if bit == "0":
                    if is_float:
                        values.append(0.0)
                    else:
                        values.append(0)
                else:
                    current_val = struct.unpack(chr_rep, encoded_bytes[byte_number:byte_number+num_size])[0]
                    values.append(current_val)
                    byte_number += num_size

        return values


    @staticmethod
    def list_from_decoded(file_name: str):
        """
        From a decoded binary file, retrieves stored numbers, adds them to a list, and returns list

        Parameters:
        file_name (str): The decoded binary file 

        Returns
        list: list of numbers in decoded binary file
        """

        #data about file
        file_path = file_name
        file_size = os.path.getsize(file_name)

        #get metadata
        is_encoded, is_float, last_values, num_size, chr_rep = FileReader.metadata_from_binary(file_name)

        #make sure file is correctly stored (should be divisible by element size)
        remainder = (file_size - 1) % num_size
        if remainder:
            raise Exception("Elements not correctly stored in binary file")
        
        #if not decoded raise error
        if is_encoded:
            raise Exception("File provided is not a bit mask decoded binary file")
        
        #open file and get bytes stored
        with open(file_path, 'rb') as f:
            decoded_bytes = f.read()
        
        #iterate through bytes and get numbers and max integer size
        current_byte = 1
        values = []

        while current_byte < file_size:
            #get four bytes and convert to integer
            current_block = decoded_bytes[current_byte:current_byte+num_size] 
            current_byte += num_size
            current_value = struct.unpack(chr_rep, current_block)[0]

            #add current value to list
            values.append(current_value)

        return values


    @staticmethod
    def list_from_csv(file_name: str, is_float: bool = True):
        """
        From a CSV file of numbers, retrieves values, and populates and returns list with numbers

        Parameters:
        file_name (str): CSV file path to be read
        is_float (bool): Type of numerical values stored in CSV (True for floats or False for integers)

        Returns:
        list: a list of numerical values found in CSV
        """


        values = []
        with open(file_name, 'r') as f:
            #read contents from CSV
            f_reader = csv.reader(f, delimiter=",")
            read_values = list(f_reader)[0]

            #iterate through values found in CSV
            for val in read_values:
                try:
                    if is_float:
                        values.append(float(val))
                    else:
                        values.append(int(val))
                except ValueError:
                    #if non-numerical value, continue and don't add to list
                    pass
        
        return values
    
    @staticmethod
    def metadata_from_binary(file_name: str):
        """
        From a binary file, retrieves metadata including:
        -Whether it is bit mask encoded or not 
        -Whether the file stores floats or integers
        -The number of values stored in the last bit mask
        -The size of each numerical value stored
        -Representative character used by struct package for data type

        Parameters:
        file_name (str): A binary file from which metadata is being extracted

        Returns
        int: 0 if file is decoded or 1 if bit mask encoded
        int: 0 if integers are stored or 1 if floats are stored
        int: the number of values stored in the last bit mask for an encoded file
        int: the size of numerical values in bytes 
        str: the representative character used by struct for data type stored in file
        """
        #read file and get first byte 
        with open(file_name, 'rb') as f:
            file_bytes = f.read()
        
        first_byte = file_bytes[0]

        #check if encoded 
        encoded = BitTools.get_bit(first_byte, 7)

        #check if float
        is_float = BitTools.get_bit(first_byte, 0)

        #get remainder/number of values in last bit mask
        num_last_values = (first_byte & int("01110000", 2)) >> 4

        #get character representation
        type_index = (first_byte & int("00001110", 2)) >> 1

        chr_rep = DataHelper.letter_from_metadata(is_float, type_index)

        #get size in bytes 
        size = struct.calcsize(chr_rep)

        return encoded, is_float, num_last_values, size, chr_rep

    
class FileConverter:
    @staticmethod
    def csv_to_binary_file(file_name: str, chr_rep='d'):
        """
        Takes a CSV file, extracts integers stored in the CSV file, and creates a decoded binary file that stores integers

        Parameters:
        file_name (str): The CSV file that will be converted to a binary file

        Returns:
        str: created binary file name
        """

        #get data from file and store in list
        is_float = (DataHelper.type_from_letter(chr_rep) == 'float')
        
        values = FileReader.list_from_csv(file_name, is_float)
        

        #convert it to binary file 
        return FileConstructor.list_to_binary_file(values, chr_rep, file_name) 

class FileConstructor:
    @staticmethod
    def list_to_binary_file(values: list, chr_rep: str, output_file_name: str=None):
        """
        Creates a decoded binary file from a list of integers.
        The function is called from other functions which extracted a list of integers from existing files.

        Parameters:
        values (list): list of integer values to be written to decoded binary file
        output_file_name (str): desired name of created binary file or existing file from which list was retrieved; should include file extension

        Returns:
        str: name of created binary file
        """

        #get name of output file and add .bin extension
        if not output_file_name:
            output_file_name = input("Enter name of file to store values in (no extensions just the name): ")
        else:
            if "." in output_file_name:
                #clear dot in file name
                dot_index = output_file_name.index(".")
                output_file_name = output_file_name[:dot_index]

        output_file_name += ".bin"

        
        #Create first byte of binary file with metadata
        bytes_string = FileConstructor.create_first_byte(False, chr_rep)

        #Go through values in list and add them in byte form to bytes object
        for value in values:
            bytes_string += struct.pack(chr_rep, value)

        #Write bytes string to file 
        with open(output_file_name, 'wb') as f:
            f.write(bytes_string)

        return output_file_name

    @staticmethod
    def create_first_byte(encoded: bool, chr_rep: str, last_mask_remainder: int=0):
        """
        Creates first byte of metadata stored in binary files that contains whether or not 
        the file is encoded, the number of values in the last bit mask, the size of each 
        number, and the type of number stored (float or integer)

        Parameters:
        encoded (bool): true if encoded, false if file is decoded
        chr_rep (str): the character representation of data type used by struct module
        last_mask_remainder (int): for encoded files, the number of bits to examine in the last bit mask

        Returns:
        bytes: the first byte of metadata that should be written to a binary file 
        """
        byte_string = ""

        #add encoded metadata 
        if encoded:
            byte_string += "1"
        else:
            byte_string += "0"

        #add the number of last values if encoded
        byte_string += f'{last_mask_remainder:03b}'

        #get number of bytes used to store each number in specified data type
        type_index = DataHelper.metadata_index_from_letter(chr_rep)
        byte_string += f'{type_index:03b}'

        #get whether number is float or integer 
        data_type = DataHelper.type_from_letter(chr_rep)

        #add 1 to end if float or 0 if integer
        if data_type == 'float':
            byte_string += "1"
        else:
            byte_string += "0"
        
        #convert string to integer and return bytes object
        byte_string_as_int = int(byte_string, 2)
        return byte_string_as_int.to_bytes(1, "little")
        





        
    
    
