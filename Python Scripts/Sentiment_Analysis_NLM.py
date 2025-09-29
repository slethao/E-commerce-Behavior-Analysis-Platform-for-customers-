import random
from textblob.classifiers import NaiveBayesClassifier
import Processing_Layer as pl
import nltk

nltk.download('punkt_tab')

"""
This class represent the NLM that is performing
sentimental analysis on review comments
"""
class Sentiment_Analysis_NLM():
    __slots__ = ('group_map')

    def __init__(self, group_map: dict[str, list[str]]):
        """
        The Constructor 'Sentiment_Analysis_NLM'
            Parameter:
                group_map (dict[str, list[str]]): The map of the dataset in which the group reference 
                                                    a list of values related to the respective group
            Private Members:
                group_map = The map of the dataset in which the group reference 
                                a list of values related to the respective group
                classifier = holds the clasifier object
                data = the data that is the results of the evalted raw data
        """
        self._group_map = group_map 
        self._classifier = None
        self._data = []

    def get_classifier(self) -> object:
        """
        This method is getting the cassifier object
            Parameter:
                NONE
            Return:
                a classifer object
        """
        return self._classifier

    def get_star_reviews(self) -> list[str]:
        """
        This method gets the 5-star reivews and takes in that value to perform the senimental
        analysis on the 5-star review
            Parameter:
                None
            Return:
                list of all the 5-stars review in the dataset
        """
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

    def format_data(self, data: list[str], review_senti_list: str) -> list:
        """
        This method is used to format the sentimental analysis on 
        the 5-star review
            Parameter:
                pass
            Return:
                list of the sentimental analysis: postive, neutral and negative
        """
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

    def shuffle_data(self) -> None:
        """
        Thi smethod is used to randomly shuffle the data before the data will be split
        80:20
            NOTE this is will be my premodel for doing
                sentimental analysis on my reviewText to do
                sentimental anlysis
                    80% --> training data
                    20% --> testing data
            Parameter:
                None
            Return:
                None
        """
        process = pl.Processing_layer(self._group_map) #NOTE this takes in a map
        csv_format = process.get_csv_format()
        random.shuffle(csv_format)
        self._data = csv_format

    def get_review_txt_train(self) -> list[tuple]:
        """
        The method is used to put the training data in the
        NLM
            Parameter:
                None
            Return:
                listing of all the training data
        """
        #NOTE [positive, neutral, negative]
        train_num = int(len(self._data)*0.8)
        train_data = self._data[0:train_num:]
        review_senti = self.get_star_reviews()
        return self.format_data(train_data, review_senti)

    def get_review_txt_test(self) -> list:
        """
        The method is used to put the testing data in the
        NLM
            Parameter:
                None
            Return:
                listing of all the testing data
        """
        test_data_num = int(len(self._data)*0.8)
        test_data = self._data[test_data_num::]
        review_senti = self.get_star_reviews()
        return self.format_data(test_data, review_senti)
    
    def train_model(self) -> None:
        """
        This method is used to train the data using the training data that is
        passed into the class
            Parameter:
                None
            Return:
                None
        """
        train_data = self.get_review_txt_train()
        self._classifier  = NaiveBayesClassifier(train_data)
        #NOTE add here (format_data)

    def evaluate_model(self) -> object:
        """
        The method is use to perfrom the evaluations on the test data
            Parameter:
                None
            Return:
                return the updated calssfier object
        """
        test_data = self.get_review_txt_test()
        return self._classifier.accuracy(test_data) # 0.8006103763987793
    
    def record_the_comments(self) -> dict[str, int]:
        """
        The method used to record all the comments' sentimental analysis
        for every review comments
            Parameter:
                None
            Return:
                map sentimetnal values for all the datasets

        """
        all_records_prob_info = {"pos": 0, "neg": 0}
        for line in self._data:
            review_txt = line[0]
            probability = self._classifier.classify(review_txt)
            all_records_prob_info[probability] += 1
        return all_records_prob_info

""" 
docker compose up -d
"""