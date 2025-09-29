import re 
"""
The class that will hold the Collection
Layer in Batch Ingestion
"""
class Collection_Layer():
    __slots__ = ('content')
    def __init__(self, content: list[str]):
        """
        Constructor for the class 'Collection Layer'
            Parameters:
                content (list[str]): a list containing all records found in the dataset
            Private members:
                content (list[str]): a list containing all records found in the dataset
                group_map (dict[str, list[str]]): a map that has a group as a key that
                                                    reference a list of revalent content
                                                    of the respected group
        """
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
    
    def parse_and_remove_groups_front(self, group_key: str, value: str, line_list: list[str]) -> list[str]:
        """
        This takes the group on front of the record that will be sorted 
        into the map that will contain the organized version of the 
        dataset
            Parameter:
                group_key (str): the group that refernces all information that related to that group
                value (str): the values that associate with the respective group
                line_list (list[str]): the original record within the dataset
            Return:
                This will return the record in a list excluding the two group at
                the start of the record and the end of the record
        """
        self._group_map[group_key].append(value)
        line_list.remove(line_list[0])
        return line_list

    def parse_and_remove_groups_end(self, group_key: str, value: str, line_list: list[str]) -> list[str]:
        """
        This takes the group on end of the record that will be sorted 
        into the map that will contain the organized version of the 
        dataset
            Parameter:
                group_key (str): the group that refernces all information that related to that group
                value (str): the values that associate with the respective group
                line_list (list[str]): the original record within the dataset
            Return:
                This will return the record in a list excluding the two group at
                the start of the record and the end of the record
        """
        self._group_map[group_key].append(value)
        line_list.remove(line_list[len(line_list)-1])
        return line_list

    def map_groups(self) -> dict[str, list[str]]:
        """
        This method creates a map that uses all the groups in the
        dataset found in the header line as a key that references
        the data the is relavent to each group 
        (currently all the values that are reference by each key is
        empty)
            Parameter:
                None
            Return:
                dict[str, list[str]] 
                    = 
                dict[group, list of relavent content]
        """
        for line in self._content:
            #NOTE make this into a loop!
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
    def verify_schema(self) -> bool:
        """
        This method is used to verify if the all the values of in the 
        record match the schema of the table in postgres
            Parameter: 
                None
            Return:
                True: if the record does match the schema
                False: if the record does NOT match the schema
        """
        return len(self._group_map["reviewerID"]) == len(self._group_map["asin"]) == len(self._group_map["reviewerName"]) == len(self._group_map["helpful"]) == len(self._group_map["reviewText"]) == len(self._group_map["overall"]) == len(self._group_map["summary"]) == len(self._group_map["unixReviewTime"]) == len(self._group_map["reviewTime"]) == len(self._group_map["day_diff"]) == len(self._group_map["helpful_yes"]) == len(self._group_map["total_vote"])
    
    def verify_datatype_group(self, group: str) -> bool:
        """
        This method is used to verify if a record has all the values filled
        out for each required group.
            Parameter:
                group (str): all the possible groups that needs to be in a reocrd
            Return:
                True: if the record does have all its information filled
                False: if the record does NOT have all its information filled

        NOTE required group: Reviewer ID, ASIN, Reviewer Name, Helpful, Review Text, Overall, Summary, Unix Review Time, Review Time, Day Difference, Helpful Yes, Total Votes
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
        correct_data_type = True
        for value in self._group_map[group.rstrip("\n")]:
            if datatype_map[group.rstrip("\n")] != type(datatype_map[group.rstrip("\n")](value)):
                correct_data_type = False
        return correct_data_type   
    
    def set_content(self, new_content: list[str]) -> None:
        """
        This method modifies the private memeber "conent"
            Parameter:
                new_content = a list of all the filtered records from the
                                raw dataset
            Return:
                None
        """
        self._content = new_content