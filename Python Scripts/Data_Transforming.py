import shutil
import Processing_Layer as pl

"""
The class is used to transform the data
through tokenization, and get rid of missing
data (if there is any)
"""
class Transforming_Task():
    __slots__ = ('temp_file_path')

    def __init__(self, temp_file_path: str):
        """
        Constructor for the class 'Transforming_Task'

        Parameters:
            temp_file_path (str): this contains the file path for the
                                    temporarily copy of the file
        """
        self._temp_file_path = temp_file_path # for the data that is sorted

    def create_temp_file(self) -> str:
        """
        This method is used to create the temporily
        file
            Parameter:
                None
            Return:
                the fiel path of the newly created copy (str)
        """
        file_to_copy = self._temp_file_path
        copy_destination = "Temp_Folder/temp_amazon_reviews.csv"
        with open(copy_destination, "r") as data:
            if data.readlines() == []:
                shutil.copyfile(file_to_copy, copy_destination)
        return copy_destination
    
    def duplicates_be_gone(self, content: list[str]) -> list[str]:
        #NOTE just look at reviewerID
        """
        This method is used to get rid of any duplicate reocrds that
        may exsist in the datset
            Parameter:
                content (list[str]): a list that contains all the records 
                                    found in the dataset
            Return:
                returns the list of records WITHOUT the duplicates in it
        """
        all_id = list()
        for line in content:
            listed_record = line.split(",")
            if listed_record[0] not in all_id:
                all_id.append(listed_record[0])
            else:
                content.remove(line)
        return content

    #NOTE use the text_cleaning for tokenized
    def tokenize_data(self, mapped_data: dict[str, str]) -> list:
        """
        This method tokenize the review comments by getting rid of
        words that do not add any meaning to the comment so when
        the comment is feed to the NLM it will interpret the
        comment more efficiently
            Parameter:
                mapped_data (dict[str, str]): contains all the groups that are refernceing 
                                                the listing of revlaent content to its
                                                respective group
            Return:
                the list tokenize review comments in the dataset
        """
        process = pl.Processing_layer(mapped_data)
        filter_data = process.text_cleaning()
        return filter_data

    def save_dataset(self, copy_file_file_path: str, content: list[str]) -> None:
        """
        This method saves all the updates and edits of the temporlariy file into
        a cnother copy of the temporility file
            Parameter:
                copy_file_file_path (str): The filepath of the copy of the copy of the temporarily file path
                content (list[str]): all the content that will be saves
            Return:
                None
        """
        with open(copy_file_file_path, "w") as altered_data:
            altered_data.writelines(content)
    
    def missing_data(self, mapped_data: dict[str, list[str]], copy_file_file_path: str) -> list[str]:
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
        return unique_records
    
    def creating_map_keys(self, groups: list[str]) -> dict[str, list[any]]:
        """
        This method wil create a map fo the groups that are withint the datset
        that will EVENTUALLy refernce a list of content that mathces its 
        respective group
            Parameter:
                groups (list[str]): contains all the groups in the datset
            Return:
                creates a map that has the key as the group and teh value as an
                empty list
        """
        valued_map = {}
        for group in groups:
            valued_map[group] = []
        return valued_map
    
    def mapped_group(self, empty_map: dict[str, any], content: list[str]) -> dict[str, any]:
        """
        The method appends all the content to the respected group in the map
            Parameter:
                empty_map (dict[str, any]): the map that used a key to reference an empty list
                content (list[str]): a list of all the reocrds in the dataset
            Return:
                return all a filled mapped with all the groups refernceing all the values
                that are asscoiated with teh respected groups
        """
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