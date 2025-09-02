import Collection_Layer as cl

def main():
    file_path = "Batch Ingestion/Ingestion Layer/amazon_review.csv"
    print(cl.Collection_Layer(file_path).verify_data())
    print("this works ^-^")

main()