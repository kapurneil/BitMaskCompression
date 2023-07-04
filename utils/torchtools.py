import torch
from utils.filetools import *
from utils.typetools import *

class TorchConverter:
    @staticmethod
    def dtype_to_character(torch_datatype: torch.dtype):
        """
        Translates a torch data type to a struct module character representation of data type

        Parameters:
        torch_datatype (torch.dtype): A torch datatype 

        Returns:
        str: struct module character representation of torch datatype
        """
        torch_types_dict = {
            torch.float16: 'e',
            torch.float32: 'f',
            torch.float64: 'd',
            torch.int8: 'b',
            torch.int16: 'h',
            torch.int32: 'i',
            torch.int64: 'l'
        }

        return torch_types_dict[torch_datatype]
    
    @staticmethod
    def character_to_dtype(chr_rep: str):
        """
        Translates a struct module character representation of numerical datatype to torch dtype

        Parameters:
        chr_rep (str): a struct module character representation of data type

        Returns:
        torch.dtype: matching torch dtype from struct module character representation
        """

        struct_types_dict = {
            'e': torch.float16,
            'f': torch.float32,
            'd': torch.float64,
            'b': torch.int8,
            'h': torch.int16,
            'i': torch.int32,
            'l': torch.int64
        }

        return struct_types_dict[chr_rep]
    
    @staticmethod
    def tensor_to_binary_file(tensor_values: torch.Tensor, output_file: str=None):
        """
        Writes values in tensor to (non-encoded) binary file

        Parameters:
        tensor_values (torch.Tensor): tensor to be written to binary file
        output_file (str): output file to 
        """

        #convert tensor to list
        values_list = tensor_values.tolist()

        #get struct module datatype character
        chr_rep = TorchConverter.dtype_to_character(tensor_values.dtype)

        #create file and return path
        return FileConstructor.list_to_binary_file(values_list, chr_rep, output_file)
        


    @staticmethod
    def binary_to_tensor(file_name: str):
        """
        Reads numerical values from binary file and converts them to tensor

        Parameters:
        file_name (str): binary file with float or integer values 

        Returns:
        torch.tensor: tensor with values stored in binary file
        """

        #get datatype
        chr_rep = FileReader.metadata_from_binary(file_name)[4]
        tensor_dtype = TorchConverter.character_to_dtype(chr_rep)

        #get values
        values_list = FileReader.get_list(file_name)

        #convert to tensor
        new_tensor = torch.tensor(values_list, dtype=tensor_dtype)
        
        #return tensor
        return new_tensor
        

    
