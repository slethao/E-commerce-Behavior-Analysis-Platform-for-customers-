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
    
    def view_table_content(self, table_name: str) -> list[tuple]:
        try:
            self._cursor.execute(f'SELECT * FROM {table_name};')
            return self._cursor.fetchall()
        except psycopg2.Error as e:
            return e.pgerror
        
    def format_to_csv(self, table_content: list[tuple])-> list[str]:
        formatted_content = []
        record_line = ""
        for line in table_content:
            record = line[1:len(line):]
            for item in record:
                record_line += f"{item}," 
            formatted_content.append(f"{record_line[:len(record_line)-1:]}\n")
            record_line  = ""
        return formatted_content