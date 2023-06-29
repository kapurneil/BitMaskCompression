from utils.filetools import *

class Decoder:
    @staticmethod
    def decode_bin_file(file_name):
        """Takes integer values from file and adds them to a binary file in byte form"""

        #get values from encoded file in list form
        values = FileReader.get_list(file_name)

        #write array to binary file
        FileConverter.array_to_binary_file(values, file_name)