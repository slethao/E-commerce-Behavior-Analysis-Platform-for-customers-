import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
"""
This class is to represent the Storage Layer
in the Batch Ingestion
"""
class Storage_Layer():
    __slots__ = ('file_path', 'columns')

    def __init__(self, file_path: str, columns: list[str]):
        """
        The Constructor 'Storage Layer'
            Parameter:
                file_path (str): the filepath of the file the program wants to store
                columns (list[str]): the groups the table want to store
            Private Members:
                file path = contains the path of the file
                table name = the name of the table that you want to store
                user name = the username for the datasbase
                password = the password used to access the database
                database name = the name of the database 
                connection = the connection to access the database
                columns = the groups in the table
                cursor = the cursor to edit objects in teh database
        """
        self._file_path = file_path
        self._table_name = ""
        self._user_name = os.getenv("DB_USER_NAME")
        self._password = os.getenv("PASSWORD")
        self._database_name = os.getenv("DB_NAME")
        self._connection = psycopg2.connect(dbname=f"{self._database_name}",
                                            user=f"{self._user_name}",
                                            password=f"{self._password}",
                                            port="5432")
        self._columns = columns #NOTE these are my group headers
        self._cursor = self._connection.cursor()

    def load_table_data(self, table_name: str, file_path: str, columns: list[str]) -> None:
        """
        The mehtod used to load the data into the table
            Parameter:
                table_name (str): the name of the table the program wants to load contents in 
                file_path (str): the file path that is used to access the chosen file
                columns (list[str]): the group in the table
            Return:
                None
        """
        quoted_columns = [f'"{col.strip()}"' for col in columns]
        print("File path: ", file_path)
        with open(file_path, 'r') as results:
            for line in results.readlines():
                overall_listing = line.strip().split(",")
                if len(overall_listing) > 12:
                    temp = overall_listing[3]
                    overall_listing[3] = f"{temp},{overall_listing[4]}"
                    overall_listing.remove(overall_listing[4])
                self._cursor.execute(
                    f'INSERT INTO "{table_name}" ({", ".join(quoted_columns)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                    (
                        str(overall_listing[0]), str(overall_listing[1]), str(overall_listing[2]), str(overall_listing[3]),
                        str(overall_listing[4]), float(overall_listing[5]), str(overall_listing[6]), str(overall_listing[7]),
                        str(overall_listing[8]), int(overall_listing[9]), int(overall_listing[10]), int(overall_listing[11])
                    )
                )
                self._connection.commit()
        
    def create_table_overall(self,table_name: str, columns: list[str]) -> None:
        """
        The method is used to create an empty table.
            Parameter:
                table_name (str) -> the name of the table that the program wants to use
                columns (list[str]) -> the groups used in the newly made table
            Return:
                None
        """
        try:
            quoted_columns = [f'"{col.strip()}"' for col in columns]
            
            column_defs = (
                f'{quoted_columns[0]} varchar',
                f'{quoted_columns[1]} varchar',
                f'{quoted_columns[2]} varchar',
                f'{quoted_columns[3]} varchar',
                f'{quoted_columns[4]} varchar',
                f'{quoted_columns[5]} float',
                f'{quoted_columns[6]} varchar',
                f'{quoted_columns[7]} varchar',
                f'{quoted_columns[8]} varchar',
                f'{quoted_columns[9]} int',
                f'{quoted_columns[10]} int',
                f'{quoted_columns[11]} int'
            )
            self._cursor.execute(
                f'CREATE TABLE IF NOT EXISTS "{table_name}" (id serial PRIMARY KEY, {", ".join(column_defs)});'
                )
            self._connection.commit()
        except psycopg2.Error as e:
            print(f"Error: {e.pgerror}")

    def verify_table_filled(self, table_name: str) -> bool:
        """
        This method verifies that the tables is filled with content.
            Parameters:
                table_name (str) = the name of the table you want to see
                                    if it has content or not
            Return:
                True: the table has content
                False: the table wither doesn't exisit or there is no content
        """
        self._cursor.execute(f'SELECT * FROM "{table_name}";')
        return bool(self._cursor.fetchall())
