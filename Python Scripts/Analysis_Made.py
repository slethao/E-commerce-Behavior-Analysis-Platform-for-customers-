import Collection_Layer as cl
import Processing_Layer as pl
import Storage_Layer as sl
import Query_Layer as ql

def record_results(file_path, results):
    with open(file_path, "w") as content:
        content.writelines(results)

def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        collection = cl.Collection_Layer(content)
        groups_sorted = collection.map_groups() #NOTE use the data here for the next layer (proccessing)
        file_path_one = "Batch Ingestion/Processing Layer/processed_data.csv" # this is for the processed data after the word filter
        file_path_two = "Batch Ingestion/Processing Layer/sentiment_analysis_review.csv"
        file_path_three = "Batch Ingestion/Processing Layer/overall_mean_review.csv"
        file_path_four = "Batch Ingestion/Collection Layer/sorted_collection.csv"
        file_list = [file_path_one, file_path_two, file_path_three, file_path_four]
        storage = sl.Storage_Layer(file_path_one, all_groups) #
        process_collect = pl.Processing_layer(groups_sorted)
        query_obj = ql.Query_Layer()
        
        all_sorted_csv_format = [process_collect.get_data(i) for i in range(len(groups_sorted["reviewerID"]))]
        csv_format_list_of_lines = [",".join(process_collect.get_data(i)) for i in range(len(groups_sorted["reviewerID"]))]

        if collection.verify_schema() == True and len([group for group in all_groups if collection.verify_datatype_group(group) == True]) == 12:
            for i in range(len(all_sorted_csv_format)):
                line = all_sorted_csv_format[i]
                if process_collect.handing_missing_data(line) == True:
                    process_collect.remove_record(i)
            altered_review_content = process_collect.text_cleaning()
            process_collect.set_value(altered_review_content, "reviewText")
            
            proccess_result = [process_collect.get_csv_format(),
                               process_collect.calculate_reviews(all_sorted_csv_format),
                               process_collect.overall_review_product(all_sorted_csv_format),
                               csv_format_list_of_lines]
            for i in range(len(file_list)):
                record_results(file_list[i], proccess_result[i])

            storage.convert_csv_to_table_overall("processed_data",
                                                file_list[0],
                                                all_groups) #NOTE processed_data.csv
            storage.convert_csv_to_table_sentiment("sentiment_analysis", 
                                                    file_list[1],
                                                    ["positive","neutral","negative"]) #NOTE sentiment_analysis_review
            storage.convert_csv_to_table_overall("sorted_collection",
                                                    file_list[3],
                                                    all_groups) #NOTE sorted_collection.csv

            #print(f"These are the tables in postgres: {query_obj.view_table_content("processed_data")}") # work
            # print(f"These are the tables in postgres: {query_obj.view_table_content("sentiment_analysis")}") # does not work
            print(f"These are the tables in postgres: {query_obj.view_table_content("sorted_collection")}") # does not work

        else:
            print("This data is unfit for consluding anything...")
    print("this works ^-^")

main()