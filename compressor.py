import sys
from utils.encoder import Encoder
from utils.decoder import Decoder
from utils.filetools import *

if __name__ == "__main__":
    file_name = sys.argv[1]
    file_type = FileReader.get_file_type(file_name)

    if file_type == "encoded":
        print("Decoding encoded file")
        Decoder.decode_bin_file(file_name)
        print("Decoding complete")
    elif file_type == "decoded":
        print("Encoding decoded file")
        Encoder.encode_bin_file(file_name)
        print("Encoding complete")
    elif file_type == "csv":
        #convert to binary
        print("Converting CSV to bin and encoding")
        new_file = FileConverter.csv_to_binary_file(file_name)
        print("Created: " + new_file)

        #encode file 
        print("Encoding file: " + new_file)
        Encoder.encode_bin_file(new_file)
    else:
        print("Invalid file.")


    
