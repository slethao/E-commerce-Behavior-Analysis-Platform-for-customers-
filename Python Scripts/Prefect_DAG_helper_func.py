from prefect import flow, task
import Data_Transforming as dt
import Storage_Layer as sl
import Collection_Layer as cl
import Processing_Layer as pl
import Medallion_Model as mm

"""
This helper functions are used to automate the
Directed Acyclic Graph (DAG) 
"""

@task
def collection_task(content: list[str], groups: list[str]) -> dict[str, list[str]]:
    """
    This method is used to run the collection task that is verifies the records
    that is is valid
        Parameter:
            content (list[str]): The listing of all values that are realted to the respective group
            groups (list[str]): the listing of all the groups in the dataset
        Return:
            return the mapping of the keys being used as the groups and the reference
            the listing of all the content taht are related to each group
    """
    collection = cl.Collection_Layer(content)
    if collection.verify_schema() and len([group for group in groups if collection.verify_datatype_group(group)]) == 12:
        return collection.map_groups()
    else:
        print("Error: Invalid schema or incomplete record.")
        return {}

@task
def transform_task(groups_sorted: dict[str, list[str]], file_path: str, groups: list[str]) -> dict[str, list[str]]:
    """
    The method is used to perform the transfomring task whic is just transforming
    data
        Parameter:
            groups_sorted (dict[str, list[str]]): the mapping that key (group) refernce the listing of content that
                                                    is relavent to the respective group
            file_path (str): the file path is location of where the file is located
            groups (list[str]): the groups that are within the dataset
        Return:
            the mapping that key (group) refernce the listing of content that
            is relavent to the respective group (value)
    """
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
    """
    The method used to do the database task 
        Parameter:
            groups (list[str]): The listing for groups in the dataset
            file_path (str): The file location of the file
        Return:
            None
    """
    storage = sl.Storage_Layer(file_path, groups)
    storage.create_table_overall("processed_data", groups)
    if not storage.verify_table_filled("processed_data"):
        storage.load_table_data("processed_data", "Temp_Folder/temp_amazon_reviews_02.csv", groups)

@task
def medallion_architecture(all_groups: list[str]):
    """
    The method used to perform the Meallion Architecture to
    the dataset (filting thoguh data lake)
        Parameters:
            pass
        Return:
            pass
    """
    medallion = mm.Medallion_Model("processed_data", all_groups)
    raw_content = medallion.get_bronze()
    silver_content = medallion.transfer_to_silver(raw_content)
    return medallion.transfer_to_gold(silver_content)

@flow
def create_the_dag(content: list[str], file_path: str, groups: list[str]) -> None:
    """
    This method would run all the helper task in
    to automate and run all the ordered sesion.
        Parameter:
            content (list[str]):the listing of all listing that are associated with each respected
                                group
            file_path (str): the location of the file 
            groups (list[str]): the listing of all the groups in the dataset
        Return:
            None
    """
    mapped_content = collection_task(content, groups)
    transform_task(mapped_content, file_path, groups)
    database_task(groups, file_path)
    return medallion_architecture(groups)