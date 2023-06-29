from utils.filetools import FileReader

class Decoder:
    @staticmethod
    def decode_bin_file(file_name):
        """Takes intger values from file and adds them to a binary file in byte form"""

        values = FileReader.get_list(file_name)

        #The first byte holds metadata about the binary file. 0 signifies decoded 
        decoded_bytes = bytes(1) #creates a bytes object with the first byte being 0

        #Go through values in list and add them in byte form to bytes object
        for element in values:
            decoded_bytes += int.to_bytes(element, 4, "little", signed=True)
        
        #Write bytes to binary file
        with open(file_name, 'wb') as f:
            f.write(decoded_bytes)