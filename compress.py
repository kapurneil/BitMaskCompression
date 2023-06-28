import csv
import sys
import os
from utils.bittools import BitTools
from utils.encoder import Encoder
from utils.decoder import Decoder
from utils.filetools import BinaryUtility

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


    
