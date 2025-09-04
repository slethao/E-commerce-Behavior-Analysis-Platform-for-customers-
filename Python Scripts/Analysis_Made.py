import Collection_Layer as cl
import re

def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    with open(file_path, 'r') as data:
        all_groups = data.readline().split(",")
        content = data.readlines()
        collection = cl.Collection_Layer(content)
        print(collection.map_groups()["summary"]) # helpful was suppose to be day_diff

    print("this works ^-^")

main()