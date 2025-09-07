class Processing_layer():
    def __init__(self, group_map):
        super().__init__()
        self._group_map = group_map

    def handing_missing_data(self, record):
        """
        found_useless = False --> the record is filled completely
        found_useless = True --> the record is NOT filled completely
        """
        # print(record)
        found_useless = False
        if record[0] == "" or record[1] == "" or record[2] == "": # reviewerID, asin, reviewerName (fake data) 0,1,2
            found_useless = True
        if record[4] == "" or record[6] == "": # reviewText, summary (nothing to look into) 4,6
            found_useless = True
        if record[5] == "" or record[10] == "" or record[11] == "": # overall, helpful, total_vote (imputation = fill missing value with the mean) 5,10,11
            possible_missed = [record[5], record[10], record[11]]
            print("hit me")
            for i in range(len(possible_missed)):
                group = possible_missed[i]
                if group == "":
                    self.imputation(self._group_map.values()[i], group)
        #NOTE you will update the map
        #NOTE return the altered_csv_format
        return found_useless

    def remove_duplicates(self):
        pass #NOTE needs a condition statement

    def text_cleaning(self):
        common_list = ["like", "you know", "I mean", "Well", "So", 
                       "Right", "Basically", "very", "really", "literally", 
                       "seriously", "totally", "completely", "absolutely",
                       "in order to", "in order", "due to the fact that",
                       "the fact that", "at the end of the day", "is",
                       "believe", "think", "just", "that", "very", "anyway",
                       "here", "thing", "when it comes to", "a", "an", "the",
                       "and", "or", "but", "in", "on", "at", "with", "from",
                       "I", "you", "he", "she", "it", "they", "is", "are", "was",
                       "were", "be", "I've", "It", "\"I", "\"it", "But", "I'm", "A"
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

    def calculate_reviews(self, csv_format):
        # e.g., 4-5 stars = positive, 1-2 stars = negative, 3 stars = neutral
        # [positive, neutral, negative]
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
        all_reviews.append(f"Positive Setiment: {pos_sum / pos_counter}")
        all_reviews.append(f"Neutral Setiment: {neutral_sum / neutral}")
        all_reviews.append(f"Negative Setiment: {neg_sum / neg_counter}")
        return all_reviews

    def overall_review_product(self, csv_format):
        """
        caluculate a key tric, and that metric is the
        average rating per product 
        (calculte teh entrie project)
        """
        overall_rating_sum = 0.0
        for line in csv_format:
            rating = float(line[5])
            overall_rating_sum += rating
        return overall_rating_sum/len(csv_format)
    
    def get_data(self, index):
        return [self._group_map[key][index] for key in self._group_map]
    
    def imputation(self, num_records, group):
        # just do the replacement here
        summation = 0.0
        for value in self._group_map[group]:
            if value != "":
                summation += float(value)
        mean = summation/num_records
        [mean if self._group_map[group][index] == "" else index for index in range(len(self._group_map[group]))]
        
    
    def remove_record(self, index):
        for group in self._group_map:
            self._group_map[group].remove(self._group_map[group][index])
    
    def get_csv_format(self):
        all_sorted_csv_format = [self.get_data(i) for i in range(len(self._group_map["reviewerID"]))]
        return all_sorted_csv_format