import Query_Layer as ql
import Data_Transforming as dt
import Processing_Layer as pl

"""
This class is use to perform the
Medallion
"""
class Medallion_Model():
    __slots__ = ('table_name', 'groups')

    def __init__(self, table_name: str, groups: list[str]):
        """
        The Constructor for 'Medallion Model'
            Parameter:
                table_name (str): has the table name that will be used to put in the data
                groups (list[str]): the groups used in the tabel
            Private Members:
                table_name = the name of the table that will be added to the database
                querry_obj = the object that will be used to make queries to database
                groups = the groups that will be used in the new table
        """
        self._table_name = table_name
        self._querry_obj = ql.Query_Layer()
        self._groups = groups

    def get_bronze(self) -> None:
        """
        This method just gets the raw data
            Parameters:
                None
            Reutrns:
                None
        """
        content = self._querry_obj.view_table_content(self._table_name)
        csv_format = self._querry_obj.format_to_csv(content)
        with open("Medallion Model/Bronze/bronze.csv", "w") as info:
            info.writelines(csv_format)
        return csv_format

    def transfer_to_silver(self, content: list[str]) -> list[str]:
        """
        The method that will be used to filter the bronze data (raw data)
        and transfer it to the Silver data lake
            Parameter:
                content (list[str]): listing of all the records in the 
                                        dataset (raw content)
            Return:
                list of the filtered content from the bronze data lake
        """
        transform = dt.Transforming_Task("Medallion Model/Bronze/bronze.csv")
        unique_records = transform.duplicates_be_gone(content)
        unique_map = transform.creating_map_keys(self._groups)
        filled_unique_map = transform.mapped_group(unique_map, unique_records)
        process = pl.Processing_layer(filled_unique_map)
        tokenized_data = process.text_cleaning()
        process.set_value(tokenized_data, "reviewText")
        csv_format = process.get_csv_format()
        with open("Medallion Model/Silver/silver.csv", "w") as info:
            info.writelines(csv_format)
        return csv_format

    def transfer_to_gold(self, content: list[str]) -> list[str]:
        """
        The method that will be used to filter the silver data and
        transfer it to the Gold data lake
            Parameter:
                content (list[str]): listing of all the records in the 
                                        silver data lake
            Return:
                list of the filtered content from the silver data lake
        """
        with open("Medallion Model/Gold/gold.csv", "w") as info:
            info.writelines(content)
        return content