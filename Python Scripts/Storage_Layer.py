#NOTE create csv and put it into postgres
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
class Storage_Layer():
    def __init__(self, file_path, columns):
        self._file_path = file_path
        self._table_name = ""
        #NOTE after it works put into a .env file
        self._user_name = os.getenv("DB_USER_NAME")
        self._password = os.getenv("PASSWORD")
        self._database_name = os.getenv("DB_NAME")
        self._connection = psycopg2.connect(dbname=f"{self._database_name}",
                                            user=f"{self._user_name}",
                                            password=f"{self._password}",
                                            port="5432")
        self._columns = columns #NOTE these are my group headers

    def convert_csv_to_table(self):
        try:
            #print(f"Status of connection: {self._connection}") # the status of the database is open and connected
            # 
            cursor = self._connection.cursor()
            #NOTE the cursor to perform the database is active (works)
            #cursor.execute("SELECT 1;") 
            #testing = cursor.fetchone()
            #print(f"cursor check: {testing}") # (works)
            #NOTE end of the debugging for the cursor
            #NOTE test to see if table was made propperly when you get to rit (only for the full columns)
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._table_name} ({reviewerID} PRIMARY KEY, varchar {asin},{helpful} varchar,{reviewText} varchar,{overall} float, {unixReviewTime} varchar, {reviewTime} varchar, {day_diff} int, {helpful_yes} int, {total_vote} int;")
            
            # cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._table_name} ({self._columns[0]} PRIMARY KEY,varchar {self._columns[1]}, varchar {self._columns[2]},{self._columns[3]} varchar,{self._columns[4]} varchar,{self._columns[5]} float, {self._columns[6]} varchar, {self._columns[7]} varchar, {self._columns[8]} int, {self._columns[9]} int, {self._columns[10]} int;")
            current_file = open(self._file_path, 'r')
            # cursor.copy_from(
            #     file=current_file, 
            #     table=self._table_name, 
            #     sep=',',
            #     null='\\N', 
            #     columns=('reviewerID','asin','reviewerName','helpful','reviewText','overall','summary','unixReviewTime','reviewTime','day_diff','helpful_yes','total_vote')
            #     )
            self._connection.commit()
            current_file.close()
            cursor.close()
            self._connection.close()
        except psycopg2.Error as e:
            print(f"Error: {e.pgerror}")
    def set_table_name(self, new_table_name):
        self._table_name = new_table_name

    def set_file_path(self, new_file_path):
        self._file_path = new_file_path
# make a table to load into the postgres table
# copy_from() within the psycopg2
# cursor.copy_from(file, table_name, sep=',', columns=None)
# commit()
