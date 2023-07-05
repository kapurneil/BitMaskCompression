import struct
from utils.filetools import FileReader, FileConstructor


class Encoder:
    @staticmethod
    def encode_bin_file(file_name: str):
        """
        Using bitmask encoding, encodes a binary file containing a byte of metadata and numerical values in byte from

        file_name (str): file path to a binary file to be encoded using bit mask encoding
        """
        #get values from file
        values_list = FileReader.list_from_decoded(file_name)

        #get metadata
        chr_rep = FileReader.metadata_from_binary(file_name)[4]

        #get remainder in last bitmask
        last_mask_remainder = len(values_list) % 8
        
        #Create bytes object to write to file, starting off with first byte which holds metadata
        encoded_bytes = FileConstructor.create_first_byte(True, chr_rep, last_mask_remainder)

        #iterate through list
        list_index = 0
        while list_index < len(values_list):
            #create bit mask and bytes object for non-zero elements
            block_bit_mask = ""

            #create an empty bytes object to store non-zero elements
            non_zero_bytes = bytes(0)

            #iterate through 8 elements at a time in the list (each bit mask stores 8 elements)
            for i in range(8):
                try:
                    #get element
                    element = values_list[list_index]

                    #add appropriate bit to bit mask
                    block_bit_mask += "0" if element == 0 else "1"

                    #if element is non-zero add in byte form to bytes object 
                    if element != 0:
                        non_zero_bytes += struct.pack(chr_rep, element)

                    list_index += 1
                except IndexError:
                    #used to handle remainders if list length is not multiple of 8
                    remaining_zeros = 8 - i
                    for j in range(remaining_zeros):
                        block_bit_mask += "0"
                    break
            
            #convert bitmask to bytes and add bitmask and list to encoded_bytes
            block_mask_as_bytes = int(block_bit_mask, 2).to_bytes(1, "little")

            #add bit mask followed by non-zero elements to bytes object that will be written to file
            encoded_bytes += block_mask_as_bytes
            encoded_bytes += non_zero_bytes
        
        #write bytes to binary file
        with open(file_name, 'wb') as f:
            f.write(encoded_bytes)
    
    