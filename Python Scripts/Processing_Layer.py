from sklearn.preprocessing import StandardScaler

class Processing_layer():
    def __init__(self, content, group_map):
        super().__init__()
        self._content = content
        self._group_map = group_map
        self._missing_content = []

    def handing_missing_data(self):
        #NOTE do this KNN imputation manually
        #NOTE step one: get the neightbors
                # Standardization:
                    # standarize dataset by using StandardScaler
                    # to transform the data so that it has a mean
                    # of 0 and a standard deviation of 1
                # Select a Data Point: Chose a data poitn that has at least one missing value
                # Distance Calculation: 
                    # Calculate the distance between this data point and every other
                    # data point in the dataset. Use a chosen metric (Euclidean). The
                    # distance calcuation should be "NaN-aware", meaning it only considers
                    # the features where both data points have non-missing values
                # Find the K-Neighbors:
                    # idenify the k data points that have the smallest disatnces to your
                    # selected datapoint. These k points form the neighbors. The value of
                    # k is the n_neighbors parameter you choosen
        #NOTE step two: KNNImputer method
                # weights = 'uniforms'
                    # a) weighting (you can use different weighting schemes)
                        # uniform (all k neighbors contribute equally to the imputed value.
                        # This is the simplest approach)
                        # distance (the contribution of each neighbor is inversely proportional
                        # to its distance from the data point with the missing value. Closer
                        # neighbors have a greater influence)
        #NOTE step three: .fit()
                # takes the dataset and, for a given n_neighbors and metric, it sets up the
                # info to find teh closest neighbors for any future imputation
        #NOTE step four: .transform()
                # for each missing value, it finds the k nearest neighbors from the data
                # it was fitted on and fills the missing value
        self._missing_values = []

    def remove_duplicates(self):
        self._content = { line for line in self._content }

    def text_cleaning(self):
        pass

    def calculate_reviews(self, csv_format):
        # (e.g., 4-5 stars = positive, 1-2 stars = negative, 3 stars = neutral)
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
        # index 5
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