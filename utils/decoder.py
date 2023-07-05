from utils.filetools import *

class Decoder:
    @staticmethod
    def decode_bin_file(file_name: str):
        """Takes a bit mask encoded binary file of numerical values and decodes it 

        Parameters:
        file_name (str): A bit mask encoded binary file
        """

        #get data type
        chr_rep = FileReader.metadata_from_binary(file_name)[4]

        #get values from encoded file in list form
        values = FileReader.list_from_encoded(file_name)

        #write array to binary file
        FileConstructor.list_to_binary_file(values, chr_rep, file_name)
    