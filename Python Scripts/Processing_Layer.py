class Processing_layer():
    __slots__ = ('group_map')
    def __init__(self, group_map: dict[str,list[str]]):
        """
        The Constructor 'Processing Layer'
            Parameter:
                group_map (dict[str, list[str]]): a map that contains all the group data in its 
        """
        super().__init__()
        self._group_map = group_map

    def handing_missing_data(self, record: list[str]) -> bool:
        """
        The method is used for handling missing data.
            Parameter:
                record (list[str]): A listing of records in the datasets
            Return:
                False --> the record is filled completely
                True --> the record is NOT filled completely
        """
        # print(record)
        found_useless = False
        if record[0] == "" or record[1] == "" or record[2] == "": # reviewerID, asin, reviewerName (fake data) 0,1,2
            found_useless = True
        if record[4] == "" or record[6] == "": # reviewText, summary (nothing to look into) 4,6
            found_useless = True
        if record[5] == "" or record[10] == "" or record[11] == "": # overall, helpful, total_vote (imputation = fill missing value with the mean) 5,10,11
            possible_missed = [record[5], record[10], record[11]]
            for i in range(len(possible_missed)):
                group = possible_missed[i]
                if group == "":
                    self.imputation(self._group_map.values()[i], group)
        return found_useless

    def text_cleaning(self) -> list[str]:
        """
        This method get rids of of words in the comments that not
        considered emaingful in the review comments
            Parameter:
                None
            Return:
                a list of review comments that are 'cleaned'
        """
        common_list = ["like", "you know", "I mean", "Well", "So", 
                       "Right", "Basically", "very", "really", "literally", 
                       "seriously", "totally", "completely", "absolutely",
                       "in order to", "in order", "due to the fact that",
                       "the fact that", "at the end of the day", "is",
                       "believe", "think", "just", "that", "very", "anyway",
                       "here", "thing", "when it comes to", "a", "an", "the",
                       "and", "or", "but", "in", "on", "at", "with", "from",
                       "I", "you", "he", "she", "it", "they", "is", "are", "was",
                       "were", "be", "I've", "It", "\"I", "\"it", "But", "I'm", "A",
                       "this", "it.", ".I", "This", "...", ".."
                       ] #4 reviewText
        tokenize_lines = [review for review in self._group_map["reviewText"]]
        filter_lines = []
        for review in tokenize_lines:
            word_list = review.split()
            for word in word_list:
                if word in common_list:
                    word_list.remove(word)
            filter_lines.append(" ".join(word_list))
        return filter_lines

    def calculate_reviews(self, csv_format: list[str]) -> list[str]:
        """
        This method used to calucate the sentimental 5-star reviews.
            Parameter:
                csv_format (list[str]): list of all the records in the dataset
            Return:
                a list that contains a sentiment analysis of 5-star review that
                contains overall positive, neutral, and negative
        NOTE e.g., 4-5 stars = positive, 1-2 stars = negative, 3 stars = neutral
            [positive, neutral, negative]
        """
        pos_counter = 0
        pos_sum = 0
        neutral = 0
        neutral_sum = 0
        neg_counter = 0
        neg_sum = 0
        all_reviews = []
        for line in csv_format:
            if float(line[5]) >= 4 and float(line[5]) <= 5:
                pos_counter += 1
                pos_sum += float(line[5])
            elif float(line[5]) == 3.0:
                neutral += 1
                neutral_sum += float(line[5])
            else:
                neg_counter += 1
                neg_sum += float(line[5])
        all_reviews.append(f"{round(pos_sum / pos_counter, 2)},")
        all_reviews.append(f"{round(neutral_sum / neutral, 2)},")
        all_reviews.append(f"{round(neg_sum / neg_counter, 2)}")
        return all_reviews

    def overall_review_product(self, csv_format: list[str]) -> str:
        """
        The method is used to calcualte the overall 5-star review.
            Parameter:
                csv_format (list[str]): a listing of all the records
            Return:
                a string value that contains the overall 5-star reivew
        """
        overall_rating_sum = 0.0
        for line in csv_format:
            rating = float(line.split(",")[6])
            overall_rating_sum += rating
        return round(overall_rating_sum/len(csv_format), 2)
    
    def get_data(self, index: int) -> list[str]:
        """
        This method is used to create a record from the map that
        contains the content
            Parameter:
                index (int): location of where the group is 
            Return:
                a list that contains the group values in a record
        """
        return [self._group_map[key][index] for key in self._group_map]
    
    def imputation(self, num_records: int, group:list[str]) -> None:
        """
        The method use calucate the impuation
            Parameters:
                num_records (int): the number of records in a dataset
                group (list[str]): a listing of groups in the dataset
            Return:
                None
        """
        summation = 0.0
        for value in self._group_map[group]:
            if value != "":
                summation += float(value)
        mean = summation/num_records
        [mean if self._group_map[group][index] == "" else index for index in range(len(self._group_map[group]))]
    
    def remove_record(self, index: int) -> None:
        """
        This method jsut removes a record from the dataset
            Parameter:
                index (int): the location where the record is located
            Return:
                None
        """
        for group in self._group_map:
            self._group_map[group].remove(self._group_map[group][index])
    
    def get_csv_format(self) -> list[str]:
        """
        The method is used to get the content stored in teh
        Processing Layer class to a list of records.
            Parameter:
                None
            Return:
                a list of records
        """
        all_sorted_csv_format = [",".join(self.get_data(i)) for i in range(len(self._group_map["reviewerID"]))]
        return all_sorted_csv_format
    
    def set_value(self, new_content: list[str], group: str) -> None:
        """
        The method just modifies the content private member in
        Processing Layer
            Parameter:
                new_content (list[str]): the update content the program wants to use
                group (str): a group the program wants to refernce and replace its content
            Return:
                None
        """
        self._group_map[group] = new_content