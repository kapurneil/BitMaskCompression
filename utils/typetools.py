class DataHelper:
    
    @staticmethod
    def letter_from_size(is_float: bool, bytes_size: int):
        """ 
        From a size and data type, provides the appropriate letter used by struct module to 
        represent a numerial data type

        Parameters:
        is_float (bool): True for floats and False for integers
        bytes_size (int): the number of bytes used to represent the number

        Returns:
        str: One character that is used by struct module to represent the data type  
        """
        #dictionaries with sizes
        integer_letter_from_size = {
            1: 'b',
            2: 'h',
            4: 'i',
            8: 'l'
        }

        float_letter_from_size = {
            2: 'e',
            4: 'f',
            8: 'd'
        }

        #return based on data type
        if is_float:
            return float_letter_from_size[bytes_size]
        else:
            return integer_letter_from_size[bytes_size]
    
    @staticmethod
    def type_from_letter(chr_rep: str):
        """
        When provided a single character string used by struct module to represent numerical
        data type, returns whether this type is an integer or float

        Parameters:
        chr_rep (str): The one character representation used by struct module to represent data type

        Returns:
        str: 'int' if integer or 'float' if float
        """

        #dictionary with types
        dict_type_from_letter = {
            'b': 'int',
            'h': 'int',
            'i': 'int',
            'l': 'int',
            'e': 'float',
            'f': 'float',
            'd': 'float'
        }

        #return int or float
        return dict_type_from_letter[chr_rep]
    
    _float_letter_from_metadata = ['e', 'f', 'd']
    _int_letter_from_metadata = ['b' 'h', 'i', 'l']

    @staticmethod
    def letter_from_metadata(is_float: bool, index: int):
        """
        From a numerical type and metadata index number, returns the struct module character representation
        to represent the data type

        Parameters:
        is_float (bool): True if float or False if integer
        index (int): the number provided in metadata that maps to a struct module character representation

        Returns:
        str: the struct module character representation
        """

        #consult appropriate list depending on numerical type
        if is_float:
            return DataHelper._float_letter_from_metadata[index]
        else:
            return DataHelper._int_letter_from_metadata[index]
    
    @staticmethod
    def metadata_index_from_letter(chr_rep: str):
        """
        From a struct module character representation of data type, returns appropriate 
        metadata to include in first byte of binary file so that this data type can be retrieved

        Parameters:
        chr_rep (str): struct module character representation of data type

        Returns:
        int: appropriate index to include in first byte metadata
        """

        #determine whether float or int
        num_type = DataHelper.type_from_letter(chr_rep)

        #return appropriate index
        if num_type == 'float':
            return DataHelper._float_letter_from_metadata.index(chr_rep)
        else:
            return DataHelper._int_letter_from_metadata.index(chr_rep)
    
    
        
    
