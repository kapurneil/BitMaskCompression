import os
from bittools import BitTools
from filetools import FileReader

class Encoder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        self.values_list, self.max_int = FileReader.list_size_from_decoded(file_name)
        
    
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