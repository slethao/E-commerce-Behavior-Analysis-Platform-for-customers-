import Prefect_DAG_helper_func as automated_dag
from kivy.app import App
import Medallion_Model as mm

# class MainApplication(App):
#     def __init__(self):
#         pass

    # def build_application(self):
    #     self._title = ""
    #     return MainWindow() 
def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        table_name = "processed_data"
        # automated_dag.create_the_dag(content, file_path, all_groups)
        # print("this works ^-^")
        medallion = mm.Medallion_Model(table_name)
        raw_content = medallion.get_bronze()
        print(medallion.transfer_to_silver(raw_content))
        # print(medallion.transfer_to_gold())

main()