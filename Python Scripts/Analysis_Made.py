import Prefect_DAG_helper_func as automated_dag
import Sentiment_Analysis_NLM as sal
from FrontEnd import Main_Application as ma

def main():
    """
    The main application for the program runs here 
    """
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    app = ma.Main_Application('#170f18', '#c495ad', '#7b5e7b')
    with open(file_path, 'r') as data: #NOTE this will take in the raw data
        all_groups = data.readline().split(",")
        content = data.readlines()
        completed_filtered = automated_dag.create_the_dag(content, file_path, all_groups)
        mapped_out = automated_dag.collection_task(completed_filtered, all_groups)
        """
        Using the NLM to calculate the records and overall records for 5-star and comments
        """
        transform = sal.Sentiment_Analysis_NLM(mapped_out)
        transform.shuffle_data()
        transform.train_model()
        classify_tool = transform.get_classifier()
        senti_star_data = transform.get_star_reviews()
        comments_senti_data = transform.record_the_comments()
        """
        Front-end for the application that will be build
        """
        app.build_app(mapped_out, classify_tool, senti_star_data, comments_senti_data)
main()

