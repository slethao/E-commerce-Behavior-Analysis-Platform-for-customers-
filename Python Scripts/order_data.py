import re 

class Order_Data():
    def __init__(self, content):
        self._content = content
    
    def parse_groups(self):
        all_data = []
        group_dict = {"reviewerID": [],
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
        for line in self._content:
            splited_ls = line.split(",")
            # NOTE first three elemenets
            #print(f"{splited_ls[0: 3: ]} --> starting elements")
            group_dict["reviewerID"].append(splited_ls[0])
            group_dict["asin"].append(splited_ls[1])
            group_dict["reviewerName"].append(splited_ls[2]) 
            splited_ls.remove(splited_ls[0])
            splited_ls.remove(splited_ls[0])
            splited_ls.remove(splited_ls[0])
            #print(f"{splited_ls[len(splited_ls)-5: len(splited_ls): ]} --> ending elements")
            group_dict["reviewTime"].append(splited_ls[len(splited_ls)-4])# reviewTime
            group_dict["day_diff"].append(splited_ls[len(splited_ls)-3])# day_diff
            group_dict["helpful_yes"].append(splited_ls[len(splited_ls)-2])# helpful_yes
            group_dict["total_vote"].append(splited_ls[len(splited_ls)-1])# total_vote
            splited_ls.remove(splited_ls[len(splited_ls)-1])
            splited_ls.remove(splited_ls[len(splited_ls)-1])
            splited_ls.remove(splited_ls[len(splited_ls)-1])
            splited_ls.remove(splited_ls[len(splited_ls)-1])
            splited_ls.remove(splited_ls[len(splited_ls)-1])
            group_dict["helpful"].append(splited_ls[0]+splited_ls[1])
            splited_ls.remove(splited_ls[0])
            splited_ls.remove(splited_ls[0])
            #print([element for element in splited_ls if re.search("^\d.\d$", element)])
            overall = "".join([element for element in splited_ls if re.search("^\d\.\d$", element)])
            index_counter = [index for index in range(len(splited_ls)) if overall == splited_ls[index]]
            group_dict["overall"].append(index_counter[0])
            #print(splited_ls[0 :index_counter[0]:])
            group_dict["reviewText"].append("".join(splited_ls[0 :index_counter[0]:]))
            #print("--------")
            group_dict["summary"].append("".join(splited_ls[index_counter[0]+1:len(splited_ls):]))
            # print(splited_ls[index_counter[0]+1:len(splited_ls):])
            #print()
            # print(splited_ls)
            # print()
        return group_dict