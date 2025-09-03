import re 
class Collection_Layer():
    def __init__(self, file_path):
        self._file_path = file_path
        self._useable_data = list()

    #@slethao TODO method to verify the records 
    def verify_data(self):
        """
        Reviewer ID, ASIN, Reviewer Name, Helpful, Review Text, Overall Rating, Summary, Unix Review Time, Review Time, Day Difference, Helpful Yes, Total Votes
        string, string, string, int, float, string, string, string, int, int, int
        """
        with open(self._file_path, "r") as raw_data:
            all_data = raw_data.readlines()
            list_of_data = list()
            # 12 elements
            list_of_data = [all_data[index].rstrip("\n").split(",") for index in range(1, len(all_data))]
            for data in list_of_data:
                if :
                    # todo get index of the first regex and then get the element after ward combine and delete it..
                print(data)
                print()
            self._useable_data = list_of_data
            #self._useable_data = [data for data in list_of_data if re.findall() ]

    #@slethao TODO method to return verify records
    def get_verify_data(self):
        return self._useable_data
    
    def get_useable_data(self):
        return self._useable_data