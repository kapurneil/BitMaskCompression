class DataHelper:
    letter_to_size = {
        #integers
        'b': 1,
        'h': 2,
        'i': 4,
        'l': 8,

        #floats
        'e': 2,
        'f': 4,
        'd': 8
    }

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

    type_from_letter = {
        'b': 'int',
        'h': 'int',
        'i': 'int',
        'l': 'int',
        'e': 'float',
        'f': 'float',
        'd': 'float'
    }

    int_size_from_metadata = {
        
    }

    @staticmethod
    def get_byte_size(letter):
        return DataHelper.letter_to_size(letter)
