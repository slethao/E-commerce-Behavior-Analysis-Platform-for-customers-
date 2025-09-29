import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
"""
The class is used to represent
the Query Layer in the Batch Ingestion
"""
class Query_Layer():
    def __init__(self):
        """
        The Constructor 'Query Layer'
            Parameter:
                None
            Private Members:
                user_name = the username to access the database
                password = the password to access teh database
                database_name = the data base name
                connection = the connection infomration to access
                                the database
                cursor = the cursor that allows you to edit objects
                            such as tables into the database
        """
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
        """
        The method use to look at the content in table that exisit
        in the database
            Parameter:
                table_name (str): the name of the program wants to view
            Return:
                all the content in the table
        """
        try:
            self._cursor.execute(f'SELECT * FROM {table_name};')
            return self._cursor.fetchall()
        except psycopg2.Error as e:
            return e.pgerror
        
    def format_to_csv(self, table_content: list[tuple])-> list[str]:
        """
        The method is used to format all the conetent sorted into a map
        and turn it into a list of reocords with its respectively ordered
        groups
            Parameter:
                table_content (list[tuple]): all the content tha was pulled
                                                from the table
            Return:
                a list of records that were created from the mapped content
        """
        formatted_content = []
        record_line = ""
        for line in table_content:
            record = line[1:len(line):]
            for item in record:
                record_line += f"{item}," 
            formatted_content.append(f"{record_line[:len(record_line)-1:]}\n")
            record_line  = ""
        return formatted_content