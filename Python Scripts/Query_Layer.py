import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
class Query_Layer():
    def __init__(self):
        super().__init__
        self._user_name = os.getenv("DB_USER_NAME")
        self._password = os.getenv("PASSWORD")
        self._database_name = os.getenv("DB_NAME")
        self._connection = psycopg2.connect(dbname=f"{self._database_name}",
                                            user=f"{self._user_name}",
                                            password=f"{self._password}",
                                            port="5432")
        self._cursor = self._connection.cursor()
    
    def view_table_content(self, table_name) -> list:
        try:
            self._cursor.execute(f'SELECT * FROM "{table_name}";')
            return self._cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Table is unidentified")
            return e.pgerror
    
    #NOTE just add aupdate method here
    def update_table(self):
        pass