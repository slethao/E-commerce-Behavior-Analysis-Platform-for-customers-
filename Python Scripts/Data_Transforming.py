import shutil
import Processing_Layer as pl
class Transforming_Task():
    def __init__(self, temp_file_path):
        self._temp_file_path = temp_file_path # for the data that is sorted

    def create_temp_file(self):
        file_to_copy = self._temp_file_path
        copy_destination = "Temp_Folder/temp_amazon_reviews.csv"
        with open(copy_destination, "r") as data:
            if data.readlines() == []:
                shutil.copyfile(file_to_copy, copy_destination)
        return copy_destination
    # def duplicates_be_gone(self, mapped_data):
    #     process = pl.Processing_layer(mapped_data)
    #     unique_records = process.remove_duplicates()
    #     return unique_records

    #NOTE use the text_cleaning for tokenized
    def tokenize_data(self, mapped_data):
        process = pl.Processing_layer(mapped_data)
        filter_data = process.text_cleaning()
        return filter_data

    #NOTE
    def save_dataset(self, copy_file_file_path, content):
        #NOTE content = ["a\n","a\n","a\n"]
        with open(copy_file_file_path, "w") as altered_data:
            altered_data.writelines(content)
    
    def missing_data(self, mapped_data, copy_file_file_path):
        process = pl.Processing_layer(mapped_data)
        lines_in_csv = process.get_csv_format()
        unique_records = []
        for line in lines_in_csv:
            data_listed = line.strip().split(",")
            if len(data_listed) > 12:
                temp = data_listed[3]
                data_listed[3] = f"{temp},{data_listed[4]}"
                data_listed.remove(data_listed[4])
                # print("The listed data: ", data_listed)
                if process.handing_missing_data(data_listed) == False: # for each reocrd
                    unique_records.append(f"{",".join(data_listed)}")
        with open(copy_file_file_path, 'w') as data:
            data.writelines(unique_records)
        # return len(unique_records)
        return unique_records
    
    #NOTE separte this so one function gets the keys and one puts in teh value
    def creating_map_keys(self, groups):
        valued_map = {}
        for group in groups:
            valued_map[group] = []
        return valued_map
    
    def mapped_group(self, empty_map, content):
        content_counter = 0
        for line in content:
            elements_list = line.split(",")
            temp = elements_list[3]
            elements_list[3] = f"{temp},{elements_list[4]}"
            elements_list.remove(elements_list[4])
            for key in empty_map:
                empty_map[key].append(elements_list[content_counter])
                content_counter += 1
            content_counter = 0
        return empty_map