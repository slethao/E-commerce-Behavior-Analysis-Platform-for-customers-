"""
Create a class that
represent the DAG
"""
from prefect import flow, task

class Airflow_DAG():
    def __init__(self, clean_data_copy, schedule_name, schedule):
        self._clean_data_copy = clean_data_copy
        self._schedule_name = schedule_name
        self._schedule = schedule

    def create_airflow_dag(self):
        pass
        #NOTE one PythonOperator task per step in the manual DAG you did
            #NOTE collection task
            #NOTE processing task
            #NOTE data transformation task
            #NOTE database task