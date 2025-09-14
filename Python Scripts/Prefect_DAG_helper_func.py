from prefect import flow, task
import Data_Transforming as dt
import Storage_Layer as sl
import Collection_Layer as cl
import Processing_Layer as pl

@task
def collection_task(content: list[str], groups: list[str]) -> dict[str, list[str]]:
    collection = cl.Collection_Layer(content)
    if collection.verify_schema() and len([group for group in groups if collection.verify_datatype_group(group)]) == 12:
        return collection.map_groups()
    else:
        print("Error: Invalid schema or incomplete record.")
        return {}

@task
def transform_task(groups_sorted: dict[str, list[str]], file_path: str, groups: list[str]) -> dict[str, list[str]]:
    transform_obj = dt.Transforming_Task(file_path)
    unique_records = transform_obj.missing_data(groups_sorted, "Temp_Folder/temp_amazon_reviews_02.csv")
    mapped_keys = transform_obj.creating_map_keys(groups)
    mapped_content = transform_obj.mapped_group(mapped_keys, unique_records)
    tokenize_records = transform_obj.tokenize_data(mapped_content)
    process_collect = pl.Processing_layer(mapped_content)
    process_collect.set_value(tokenize_records, "reviewText")
    saved_results = process_collect.get_csv_format()
    transform_obj.save_dataset("Temp_Folder/temp_amazon_reviews_02.csv", saved_results)
    return mapped_content

@task
def database_task(groups: list[str], file_path: str) -> None:
    storage = sl.Storage_Layer(file_path, groups)
    storage.create_table_overall("processed_data", groups)
    if not storage.verify_table_filled("processed_data"):
        storage.load_table_data("processed_data", "Temp_Folder/temp_amazon_reviews_02.csv", groups)

@flow
def create_the_dag(content: list[str], file_path: str, groups: list[str]) -> None:
    mapped_content = collection_task(content, groups)
    transform_task(mapped_content, file_path, groups)
    database_task(groups, file_path)

"""
sudo lsof -i tcp:4200
kill -9 <PID>
prefect server start (to see the task that are running)
"""