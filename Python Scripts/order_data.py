import re 

class Order_Data():
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

            alter_line_04 = self.parse_and_remove_groups_end("reviewTime",splited_ls[len(splited_ls)-1], alter_line_03)
            alter_line_05 = self.parse_and_remove_groups_end("day_diff",splited_ls[len(splited_ls)-1], alter_line_04)
            alter_line_06 = self.parse_and_remove_groups_end("helpful_yes",splited_ls[len(splited_ls)-1], alter_line_05)
            alter_line_07 = self.parse_and_remove_groups_end("total_vote",splited_ls[len(splited_ls)-1], alter_line_06)
            overall = "".join([element for element in alter_line_07 if re.search("^\d\.\d$", element)])
            index_counter = [index for index in range(len(alter_line_07)) if overall == splited_ls[index]]
            self._group_map["overall"].append(index_counter[0])
            self._group_map["reviewText"].append("".join(splited_ls[0 :index_counter[0]:]))
            self._group_map["summary"].append("".join(splited_ls[index_counter[0]+1:len(splited_ls):]))

            # splited_ls = line.split(",")
            # self._group_map["reviewerID"].append(splited_ls[0])
            # self._group_map["asin"].append(splited_ls[1])
            # self._group_map["reviewerName"].append(splited_ls[2]) 
            # splited_ls.remove(splited_ls[0])
            # splited_ls.remove(splited_ls[0])
            # splited_ls.remove(splited_ls[0])
            # #print(f"{splited_ls[len(splited_ls)-5: len(splited_ls): ]} --> ending elements")
            # self._group_map["reviewTime"].append(splited_ls[len(splited_ls)-4])# reviewTime
            # self._group_map["day_diff"].append(splited_ls[len(splited_ls)-3])# day_diff
            # self._group_map["helpful_yes"].append(splited_ls[len(splited_ls)-2])# helpful_yes
            # self._group_map["total_vote"].append(splited_ls[len(splited_ls)-1])# total_vote
            # splited_ls.remove(splited_ls[len(splited_ls)-1])
            # splited_ls.remove(splited_ls[len(splited_ls)-1])
            # splited_ls.remove(splited_ls[len(splited_ls)-1])
            # splited_ls.remove(splited_ls[len(splited_ls)-1])
            # splited_ls.remove(splited_ls[len(splited_ls)-1])
            # self._group_map["helpful"].append(splited_ls[0]+splited_ls[1])
            # splited_ls.remove(splited_ls[0])
            # splited_ls.remove(splited_ls[0])

            # overall = "".join([element for element in splited_ls if re.search("^\d\.\d$", element)])
            # index_counter = [index for index in range(len(splited_ls)) if overall == splited_ls[index]]
            # self._group_map["overall"].append(index_counter[0])
            
            # self._group_map["reviewText"].append("".join(splited_ls[0 :index_counter[0]:]))
            
            # self._group_map["summary"].append("".join(splited_ls[index_counter[0]+1:len(splited_ls):]))
            
        return self._group_map