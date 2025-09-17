import Prefect_DAG_helper_func as automated_dag
import Sentiment_Analysis_NLM as sal

def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        table_name = "processed_data"
        completed_filtered = automated_dag.create_the_dag(content, file_path, all_groups)
        mapped_out = automated_dag.collection_task(completed_filtered, all_groups)
        ####################
        transform = sal.Sentiment_Analysis_NLM(mapped_out)
        transform.shuffle_data()
        transform.train_model()
        print(transform.evaluate_model())
        print("this works ^-^ =^._.^=")

main()