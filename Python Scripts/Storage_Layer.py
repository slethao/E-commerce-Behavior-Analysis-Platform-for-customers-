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

    def convert_csv_to_table_overall(self,table_name, file_path, columns):
        try:
            # Quote column names for SQL if needed
            quoted_columns = [f'"{col.strip()}"' for col in columns]
            # Build column definitions (adjust types as needed)
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
            print(f"Creating table: {table_name} with columns: {columns}")
            self._cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} (id serial PRIMARY KEY, " + ", ".join(column_defs) + ");"
            )
            with open(file_path, 'r') as results:
                # print("********")
                # print(f"CREATE TABLE IF NOT EXISTS {table_name} (" + ", ".join(column_defs) + ");")
                # print("********")
                for line in results.readlines():
                    overall_listing = line.strip().split(",")
                    if len(overall_listing) > 12:
                        temp = overall_listing[3]
                        overall_listing[3] = f"{temp},{overall_listing[4]}"
                        overall_listing.pop(4)
                    self._cursor.execute(
                        f"INSERT INTO {table_name} ({", ".join(quoted_columns)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                         +f"ON CONFLICT (id) DO UPDATE SET {columns[0]} = EXCLUDED.{columns[0]}, {columns[1]} = EXCLUDED.{columns[1]},"  
                         +f"{columns[2]} = EXCLUDED.{columns[2]}, {columns[3]} = EXCLUDED.{columns[3]}, {columns[4]} = EXCLUDED.{columns[4]}," 
                         +f"{columns[5]} = EXCLUDED.{columns[5]}, {columns[6]} = EXCLUDED.{columns[6]}, {columns[7]} = EXCLUDED.{columns[7]}," 
                         +f"{columns[8]} = EXCLUDED.{columns[8]}, {columns[9]} = EXCLUDED.{columns[9]}, {columns[10]} = EXCLUDED.{columns[10]}," 
                         +f"{columns[11]} = EXCLUDED.{columns[11]}, id = EXCLUDED.id;",
                        (
                            str(overall_listing[0]), str(overall_listing[1]), str(overall_listing[2]), str(overall_listing[3]),
                            str(overall_listing[4]), float(overall_listing[5]), str(overall_listing[6]), str(overall_listing[7]),
                            str(overall_listing[8]), int(overall_listing[9]), int(overall_listing[10]), int(overall_listing[11])
                        )
                    )
            print("table's data is updated")
            self._connection.commit()
            self._cursor.close()
            self._connection.close()
        except psycopg2.Error as e:
            print(f"Error: {e.pgerror}")
    
    def convert_csv_to_table_sentiment(self, table_name, file_path, columns):
        try:
            print("boopie")
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id serial PRIMARY KEY, {columns[0]} float, {columns[1]} float, {columns[2]} float);")
            print(f"Creating table: {table_name} with columns: {columns}")
            with open(file_path, 'r') as results:
                all_lines = results.readlines()[0].split(",")
                self._cursor.execute(f"INSERT INTO {table_name}" + 
                                        f"({columns[0]}, {columns[1]}," + 
                                        f"{columns[2]}) VALUES (%s, %s, %s)" + 
                                        f"ON CONFLICT (id) DO UPDATE SET {columns[0]} = EXCLUDED.{columns[0]}, {columns[1]} = EXCLUDED.{columns[1]}, {columns[2]} = EXCLUDED.{columns[2]}, id = EXCLUDED.id;", 
                                        (float(all_lines[0]),float(all_lines[1]), float(all_lines[2])))
            print("table's data is updated ****")
            self._connection.commit()
            self._cursor.close()
            self._connection.close()
        except psycopg2.Error as e:
            print(f"Error: {e.pgerror}")
