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
        self._cursor = self._connection.cursor()

    def load_table_data(self, table_name, file_path, columns):
        quoted_columns = [f'"{col.strip()}"' for col in columns]
            # Build column definitions (adjust types as needed)
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
                # print("table's data is updated")
                self._connection.commit()
        
    def create_table_overall(self,table_name, columns):
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
            # print(f"Creating table: {table_name} with columns: {columns}")
            self._cursor.execute(
                f'CREATE TABLE IF NOT EXISTS "{table_name}" (id serial PRIMARY KEY, {", ".join(column_defs)});'
                )
            self._connection.commit()
        except psycopg2.Error as e:
            print(f"Error: {e.pgerror}")

    def verify_table_filled(self, table_name):
        self._cursor.execute(f'SELECT * FROM "{table_name}";')
        return bool(self._cursor.fetchall())
