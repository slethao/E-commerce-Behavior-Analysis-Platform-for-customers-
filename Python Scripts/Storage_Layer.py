#NOTE create csv and put it into postgres
import psycopg2

class Storage_Layer():
    def __init__(self, file_path, table_name):
        self._file_path = file_path
        self._table_name = table_name
    
    def convert_csv_to_table(self):
        pass

    def connect_database(self):
        pass
    
    def close_database(self):
        pass
# make a table to load into the postgres table
# copy_from() within the psycopg2
# cursor.copy_from(file, table_name, sep=',', columns=None)
# commit()