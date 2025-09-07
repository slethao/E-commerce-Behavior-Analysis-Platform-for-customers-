class Processing_layer():
    def __init__(self, group_map):
        super().__init__()
        self._group_map = group_map
        self._missing_content = []

    def handing_missing_data(self, csv_format, missing_list):
        #if : # reviewerID, asin, reviewerName
            pass
        #if: # reviewText, summary
            pass
        #if : # overall, helpful, total_vote
            pass
        #NOTE you will update the map
        #NOTE return the altered_csv_format

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
        all_reviews.append(pos_sum / pos_counter)
        all_reviews.append(neg_sum / neutral)
        all_reviews.append(neg_sum / neg_counter)
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
    
    def find_missing_dataset(self, csv_content):
        self._missing_values = [line for line in csv_content if "" in line]
    
    def get_missing_values(self):
        return self._missing_values