import re 

class Collection_Layer()    :
    def __init__(self, content):
        self._content = content
        self._group_map = {"reviewerID": [],
                            "asin": [],
                            "reviewerName": [],
                            "helpful": [],
                            "reviewText": [],
                            "overall": [],
                            "summary": [],
                            "unixReviewTime": [],
                            "reviewTime": [],
                            "day_diff": [],
                            "helpful_yes": [],
                            "total_vote": []}
    
    def parse_and_remove_groups_front(self, group_key, value, line_list):
        self._group_map[group_key].append(value)
        line_list.remove(line_list[0])
        return line_list

    def parse_and_remove_groups_end(self, group_key, value, line_list):
        self._group_map[group_key].append(value)
        line_list.remove(line_list[len(line_list)-1])
        return line_list

    def map_groups(self):
        for line in self._content:
            splited_ls = line.split(",")
            alter_line = self.parse_and_remove_groups_front("reviewerID",splited_ls[0],splited_ls)
            alter_line_02 = self.parse_and_remove_groups_front("asin",splited_ls[0], alter_line)
            alter_line_03 = self.parse_and_remove_groups_front("reviewerName",splited_ls[0],alter_line_02)

            alter_line_04 = self.parse_and_remove_groups_end("total_vote",splited_ls[len(splited_ls)-1], alter_line_03)
            alter_line_05 = self.parse_and_remove_groups_end("helpful_yes",splited_ls[len(splited_ls)-1], alter_line_04)
            alter_line_06 = self.parse_and_remove_groups_end("day_diff",splited_ls[len(splited_ls)-1], alter_line_05)
            alter_line_07 = self.parse_and_remove_groups_end("reviewTime",splited_ls[len(splited_ls)-1], alter_line_06)# reviewTime
            alter_line_08 = self.parse_and_remove_groups_end("unixReviewTime",splited_ls[len(splited_ls)-1], alter_line_07)
            self._group_map["helpful"].append(f"{alter_line_08[0]},{alter_line_08[1]}")
            alter_line_08.remove(alter_line_08[0])
            alter_line_08.remove(alter_line_08[0])
        
            overall = "".join([element for element in alter_line_08 if re.search("^\d\.\d$", element)])
            index_counter = [index for index in range(len(alter_line_08)) if overall == splited_ls[index]]
            self._group_map["overall"].append(overall)
            self._group_map["reviewText"].append("".join(splited_ls[0 :index_counter[0]:]))
            self._group_map["summary"].append("".join(splited_ls[index_counter[0]+1:len(splited_ls):]))

        return self._group_map
    
    #@slethao TODO method to return verify records
    def verify_schema(self):
        return len(self._group_map["reviewerID"]) == len(self._group_map["asin"]) == len(self._group_map["reviewerName"]) == len(self._group_map["helpful"]) == len(self._group_map["reviewText"]) == len(self._group_map["overall"]) == len(self._group_map["summary"]) == len(self._group_map["unixReviewTime"]) == len(self._group_map["reviewTime"]) == len(self._group_map["day_diff"]) == len(self._group_map["helpful_yes"]) == len(self._group_map["total_vote"])
    
    def verify_datatype(self, group):
        """
        Reviewer ID, ASIN, Reviewer Name, Helpful, Review Text, Overall, Summary, Unix Review Time, Review Time, Day Difference, Helpful Yes, Total Votes
        string, string, string, string, string, float, string, string, string, string, int, int
        """
        datatype_map = {"reviewerID": str,
                            "asin": str,
                            "reviewerName": str,
                            "helpful": str,
                            "reviewText": str,
                            "overall": float,
                            "summary": str,
                            "unixReviewTime": str,
                            "reviewTime": str,
                            "day_diff": str,
                            "helpful_yes": int,
                            "total_vote": int}
        correct_data_type = False
        for value in self._group_map[group]:
            if datatype_map[group] == type(datatype_map[group](value)):
                correct_data_type = True
        return correct_data_type   

    def verify_no_missing_values(self):
        pass