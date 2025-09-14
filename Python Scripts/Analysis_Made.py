import Prefect_DAG_helper_func as automated_dag
from kivy.app import App
import Main_Window

class MainApplication(App):
    def __init__(self):
        pass

    def build_application(self):
        self._title = ""
        # return MainWindow() 
def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        automated_dag.create_the_dag(content, file_path, all_groups)
    print("this works ^-^")

main()