import Collection_Layer as cl
import Processing_Layer as pl
import Storage_Layer as sl
import Query_Layer as ql
import Data_Transforming as dt

def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        collection = cl.Collection_Layer(content)
        groups_sorted = collection.map_groups() #NOTE use the data here for the next layer (proccessing)
        file_path_four = "Batch Ingestion/Collection Layer/sorted_collection.csv"
        file_path_one = "Temp_Folder/temp_amazon_reviews_02.csv"

        storage = sl.Storage_Layer(file_path_one, all_groups) #
        query_obj = ql.Query_Layer()
        transform_obj = dt.Transforming_Task(file_path_four)

        if collection.verify_schema() == True and len([group for group in all_groups if collection.verify_datatype_group(group) == True]) == 12:
            transform_obj.create_temp_file() #NOTE temp file is created
            #NOTE missing data (groups_sorted)
            unique_records = transform_obj.missing_data(groups_sorted, "Temp_Folder/temp_amazon_reviews_02.csv")
            #NOTE tokenized (do this soon...)
            mapped_keys = transform_obj.creating_map_keys(all_groups)
            mapped_content = transform_obj.mapped_group(mapped_keys, unique_records)
            tokenize_records = transform_obj.tokenize_data(mapped_content)
            process_collect = pl.Processing_layer(mapped_content)
            process_collect.set_value(tokenize_records, "reviewText")
            saved_results = process_collect.get_csv_format()
            transform_obj.save_dataset(file_path_one, saved_results) 
            storage.create_table_overall("processed_data", all_groups) #NOTE processed_data.csv
            if storage.verify_table_filled("processed_data") == False:
                storage.load_table_data("processed_data",
                                        file_path_one,
                                        all_groups) # tokenized data, text filtered and cleaned data
                #print(f"These are the tables in postgres(proccessed_data): {query_obj.view_table_content("processed_data")}") # work
                print(f"The number of records(proccessed_data): {len(query_obj.view_table_content("processed_data"))}")
            else:
                #print(f"These are the tables in postgres(proccessed_data): {query_obj.view_table_content("processed_data")}") # work
                print(f"The number of records(proccessed_data): {len(query_obj.view_table_content("processed_data"))}")
        
            #NOTE now you you are done with the tranforming task now you have to do  Database Loading Task to finsih the DAG

    print("this works ^-^")

main()