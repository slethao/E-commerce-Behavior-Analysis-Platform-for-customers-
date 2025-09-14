import Query_Layer as ql
import Data_Transforming as dt
import Processing_Layer as pl

class Medallion_Model():
    def __init__(self, table_name: str, groups: list[str]):
        self._table_name = table_name
        self._querry_obj = ql.Query_Layer()
        self._groups = groups

    def get_bronze(self):
        content = self._querry_obj.view_table_content(self._table_name)
        csv_format = self._querry_obj.format_to_csv(content)
        with open("Medallion Model/Bronze/bronze.csv", "w") as info:
            info.writelines(csv_format)
        return csv_format

    def transfer_to_silver(self, content: list[str]) -> list[str]:
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
        with open("Medallion Model/Gold/gold.csv", "w") as info:
            info.writelines(content)
        return content