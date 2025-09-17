import random
from textblob.classifiers import NaiveBayesClassifier
import Processing_Layer as pl
import nltk

nltk.download('punkt_tab')

class Sentiment_Analysis_NLM():
    def __init__(self, group_map: dict[str, list[str]]):
        self._group_map = group_map 
        self._classifier = None
        self._data = []

    """
    NOTE this is will be my premodel for doing
    sentimental analysis on my reviewText to do
    sentimental anlysis
        80% --> training data
        20% --> testing data
    """
    def get_star_reviews(self):
        process = pl.Processing_layer(self._group_map) #NOTE this takes in a map
        csv_format = process.get_csv_format()
        listed_values_formatted = []
        for line in csv_format:
            listed_values = line.split(",")
            temp = listed_values[3]
            listed_values[3] = f"{temp},{listed_values[4]}"
            listed_values.remove(listed_values[4])
            listed_values_formatted.append(listed_values)
        #NOTE [positive, neutral, negative]
        return process.calculate_reviews(listed_values_formatted)

    def format_data(self, data, review_senti_list):
        formatted_list = []
        for line in data:
            review_txt = line.split(",")[5]
            star_review = line.split(",")[6]
            if float(star_review) <= float(review_senti_list[2].rstrip(",")):
                formatted_list.append((review_txt, "neg"))
            if float(review_senti_list[2].rstrip(",")) < float(star_review) <= float(review_senti_list[0].rstrip(",")):
                formatted_list.append((review_txt, "neutral"))
            if float(star_review) > float(review_senti_list[0].rstrip(",")):
                formatted_list.append((review_txt, "pos"))
        return formatted_list

    def shuffle_data(self):
        process = pl.Processing_layer(self._group_map) #NOTE this takes in a map
        csv_format = process.get_csv_format()
        random.shuffle(csv_format)
        self._data = csv_format

    def get_review_txt_train(self) -> list[tuple]:
        #NOTE [positive, neutral, negative]
        train_num = int(len(self._data)*0.8)
        train_data = self._data[0:train_num:]
        review_senti = self.get_star_reviews()
        return self.format_data(train_data, review_senti)

    def get_review_txt_test(self):
        test_data_num = int(len(self._data)*0.8)
        test_data = self._data[test_data_num::]
        review_senti = self.get_star_reviews()
        return self.format_data(test_data, review_senti)
    
    def train_model(self): # do this
        # NOTE take 20% of your data that you designated as the testing set
        train_data = self.get_review_txt_train()
        self._classifier  = NaiveBayesClassifier(train_data)
        #NOTE add here (format_data)

    def evaluate_model(self):
        test_data = self.get_review_txt_test()
        return self._classifier.accuracy(test_data) # 0.8006103763987793
    
    def record_into_csv(self):
        all_records_prob_info = []
        for line in self._data:
            review_txt = line[0]
            probability = self._classifier.prob_classify(review_txt)
            pos_prob = round(probability.prob("pos"), 2)
            neg_prob = round(probability.prob("neg"), 2)
            neutral_prob = round(probability.prob("neutral"), 2)
            all_records_prob_info.append([probability.max(), pos_prob, neg_prob, neutral_prob])
        return all_records_prob_info

""" 
docker compose up -d
"""