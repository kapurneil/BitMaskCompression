from utils.filetools import FileReader
import sys


if __name__ == "__main__":
    file_name = sys.argv[1]

    if FileReader.get_file_type(file_name) == "csv":
        try:
            if sys.argv[2] == "i":
                values = FileReader.list_from_csv(file_name, False)
        except IndexError:
                values = FileReader.list_from_csv(file_name)
    
    else:     
        #get list of values
        values = FileReader.get_list(file_name)

    if values:
        print(values)
    else:
        print("ERROR: Incompatible file")