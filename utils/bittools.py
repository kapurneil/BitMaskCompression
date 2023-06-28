class BitTools:
    @staticmethod
    def get_bit(byte_chunk, bit_number):
        return byte_chunk >> bit_number
    
    @staticmethod
    def set_bit(byte_chunk, bit_number):
        return byte_chunk | (1 << bit_number)

    @staticmethod
    def unset_bit(byte_chunk, bit_number):
        return byte_chunk &(~(1 << bit_number))

    @staticmethod
    def num_bytes(num):
        bit_length = num.bit_length()
        byte_length = bit_length/8
        
        #convert to integer
        if byte_length % 8 == 0:
            return int(byte_length)
        else:
            return int(byte_length) + 1