import Collection_Layer as cl
import Processing_Layer as pl
import Storage_Layer as sl

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
            file_name_list = ["Processed Data", "Sentiment Analysis", "Overall Mean", "Sorted Collection"]
            
            for i in range(len(file_list)):
                storage.set_table_name(file_name_list[i])
                storage.set_file_path(file_list[i])
                record_results(file_list[i], proccess_result[i])
                print("hit me")
                storage.convert_csv_to_table()

        else:
            print("This data is unfit for consluding anything...")
    print("this works ^-^")

main()