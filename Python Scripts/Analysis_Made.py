import Prefect_DAG_helper_func as automated_dag
import Sentiment_Analysis_NLM as sal
from FrontEnd import Main_Application as ma

def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    app = ma.Main_Application('#170f18', '#c495ad', '#7b5e7b', 0.0, 0.0, 0.0)
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        table_name = "processed_data"
        completed_filtered = automated_dag.create_the_dag(content, file_path, all_groups)
        mapped_out = automated_dag.collection_task(completed_filtered, all_groups)
        #####------#######------########
        transform = sal.Sentiment_Analysis_NLM(mapped_out)
        transform.shuffle_data()
        transform.train_model()
        print(transform.evaluate_model())
        print("this works ^-^ =^._.^=")
        classify_tool = transform.get_classifier()
        app.build_app(mapped_out, classify_tool)
main()

# from nicegui import ui

# @ui.page('/')
# async def index():
#     with ui.scroll_area().classes('w-full h-96 border p-4'):  # Adjust height as needed
#         for i in range(1, 11):  # Create 10 buttons as an example
#             button_label = f'Button {i}'
#             button = ui.button(button_label)
            
#             async def handle_click(button_id=i):
#                 ui.label(f'Clicked: Button {button_id}')
            
#             button.on('click', handle_click)

# ui.run()
