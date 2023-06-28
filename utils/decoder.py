import os 
from filetools import FileReader

class Decoder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.values = FileReader.get_list(file_name)
        
    def decode_values(self):
        decoded_bytes = bytes(1)
        for element in self.values:
            decoded_bytes += int.to_bytes(element, 4, "little", signed=True)
        
        with open(self.file_name, 'wb') as f:
            f.write(decoded_bytes)