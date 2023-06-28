from utils.filetools import FileReader
import sys


if __name__ == "__main__":
    file_name = sys.argv[1]

    #get list of values
    values = FileReader.get_list(file_name)

    if values:
        print(values)
    else:
        print("ERROR: Incompatible file")