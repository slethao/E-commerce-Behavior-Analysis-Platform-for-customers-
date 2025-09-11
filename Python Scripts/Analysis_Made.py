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
        file_path_one = "Batch Ingestion/Processing Layer/processed_data.csv"

        storage = sl.Storage_Layer(file_path_one, all_groups) #
        process_collect = pl.Processing_layer(groups_sorted)
        query_obj = ql.Query_Layer()
        transform_obj = dt.Transforming_Task(file_path_four)

        #     #NOTE after break just figure out how to make it ony insert once...
        #     storage.create_table_overall("processed_data", all_groups) #NOTE processed_data.csv
        #     if storage.verify_table_filled("processed_data") == False:
        #         storage.load_table_data("processed_data",
        #                                 file_path_one,
        #                                 all_groups) # tokenized data, text filtered and cleaned data
        #         #print(f"These are the tables in postgres(proccessed_data): {query_obj.view_table_content("processed_data")}") # work
        #         print(f"The number of records(proccessed_data): {len(query_obj.view_table_content("processed_data"))}")
        #     else:
        #         #print(f"These are the tables in postgres(proccessed_data): {query_obj.view_table_content("processed_data")}") # work
        #         print(f"The number of records(proccessed_data): {len(query_obj.view_table_content("processed_data"))}")
        
        if collection.verify_schema() == True and len([group for group in all_groups if collection.verify_datatype_group(group) == True]) == 12:
            transform_obj.create_temp_file() #NOTE temp file is created
            #NOTE missing data (groups_sorted)
            unique_records = transform_obj.missing_data(groups_sorted, "Temp_Folder/temp_amazon_reviews_02.csv")
            #NOTE tokenized (do this soon...)
            mapped_content = transform_obj.mapped_group(all_groups, unique_records)
            tokenize_records = transform_obj.tokenize_data(mapped_content) # NOTE update with this and put into file_path_one
            
            for line in tokenize_records:
                print(line)
                print()
            #NOTE create the condition before query to databsae..


    print("this works ^-^")

main()