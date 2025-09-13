import Data_Transforming as dt
import Storage_Layer as sl
import Collection_Layer as cl
import Query_Layer as ql
import Processing_Layer as pl

from prefect import flow, task
#NOTE to run the sever prefect server start (you will have to automate teh bash command so during execution you don't have to run it)
class Prefect_DAG():
    def __init__(self, content: list[str], file_path: str, groups: list[str]):
        self._content = content
        self._file_path = file_path
        self._groups = groups
        self._transform_obj = dt.Transforming_Task(self._file_path)
        self._storage = sl.Storage_Layer(self._file_path, self._groups)

    @task(tags={"collection_layer"}, description="This method sorts and format the data. (method one)")
    def collection_task(self, content: list[str]) -> dict[str, list[str]]:
        collection = cl.Collection_Layer(content)
        if collection.verify_schema() == True and len([group for group in self._groups if collection.verify_datatype_group(group) == True]) == 12:
            groups_sorted = collection.map_groups()
            return groups_sorted
        else:
            print("Error: This data an an invalid schema or one of the record is incomplete.")
            return {}


    @task(tags={"transform_task"}, description="This method transforms the data through aggregation, and filtering. (method two)")
    def transform_task(self, groups_sorted) -> None: 
        unique_records = self._transform_obj.missing_data(groups_sorted, "Temp_Folder/temp_amazon_reviews_02.csv")
        mapped_keys = self._transform_obj.creating_map_keys(self._groups)
        mapped_content = self._transform_obj.mapped_group(mapped_keys, unique_records)
        tokenize_records = self._transform_obj.tokenize_data(mapped_content)
        process_collect = pl.Processing_layer(mapped_content)
        process_collect.set_value(tokenize_records, "reviewText")
        saved_results = process_collect.get_csv_format()
        self._transform_obj.save_dataset("Temp_Folder/temp_amazon_reviews_02.csv", saved_results) 

    @task(tags={"database_task_and_layer"}, description="This method stores the final formatted *and transformed* data into the postgres database (method three)")
    def database_task(self) -> None:
        self._storage.create_table_overall("processed_data", self._groups) #NOTE processed_data.csv
        if self._storage.verify_table_filled("processed_data") == False:
            self._storage.load_table_data("processed_data",
                                    "Temp_Folder/temp_amazon_reviews_02.csv",
                                    self._groups) # tokenized data, text filtered and cleaned data

    @flow # (tags={"automated_dag"}, description="This is whole combined main process of the DAG being created")
    def create_the_dag(self) -> None:
        #NOTE put task in here in the correct order (the file path is going to be passed around)
        print("one ---------------")
        content_map = self.collection_task(self._content) #NOTE collection task
        print("two ---------------")
        # self.transform_task(content_map) #NOTE data transformatino task
        # print("three ---------------")
        # self.database_task() #NOTE databse task
        # print("four ---------------")

    def pull_from_db(self, table_name: str) -> list[tuple]:
        query_obj = ql.Query_Layer()
        view_table = query_obj.view_table_content(table_name=table_name)
        return view_table

"""
sudo lsof -i tcp:4200
kill -9 <PID>
prefect server start
"""