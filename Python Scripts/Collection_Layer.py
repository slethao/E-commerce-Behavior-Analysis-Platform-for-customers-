import pandas

class Collection_Layer():
    def __init__(self, file_path):
        self._file_path = file_path
        self._useable_data = ""

    #@slethao TODO method to verify the records 
    def verify_data(self):
        with open(self._file_path, "r") as raw_data:
            print(raw_data.readlines())

    #@slethao TODO method to return verify records
    def get_verify_data(self):
        return self._useable_data