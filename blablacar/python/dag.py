from datetime import datetime, timedelta
from airflow import DAG, TaskInstance
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from google.cloud import bigquery

from ovapi_to_json import OVAPIClient
from json_to_bq import BigQueryTable

default_args = {
    'owner': 'Airflow',             # The owner of the DAG
    'depends_on_past': False        # Don't depend on past executions
}

with DAG(
    dag_id='staging.ovapi_lines',   # The ID of the DAG
    default_args=default_args,      # The default arguments
    start_date=datetime(2023, 2, 28),   # The date and time at which the DAG will start
    schedule_interval='0 1 * * *'   # The schedule for running the DAG, every day at 1:00 AM
    ) as dag:

    # Define the first task, which calls the OVAPIClient.flatten_json method
    ovapi_to_json = PythonOperator(
        task_id='api_json', # The ID of the task
        python_callable=OVAPIClient().flatten_json,  # The function to be called
        retries=3,          # The number of times to retry the task if it fails
        retry_delay=timedelta(minutes=10)            # The delay between retries
    )

    # Define a function that runs the BigQueryTable.json_to_big_query method
    def run_json_to_bq(ds, **kwargs):
        # Get the xcom value from the previous task
        ovapi_data = kwargs['task_instance'].xcom_pull(task_ids='api_json')
    
        # Call the json_to_big_query method with the necessary arguments
        BigQueryTable().json_to_big_query(
            ovapi_data,     # The JSON data to be loaded into BigQuery
            dataset_id='my_dataset',    # The ID of the BigQuery dataset
            table_id='my_table',        # The ID of the BigQuery table
            partition_fields='execution_date',    # The partition field(s) for the table
            partition_type='DAY',       # The partition type (e.g. DAY, HOUR, etc.)
            clustering_fields=['TransportType', 'LineWheelchairAccessible'],    # The clustering fields for the table
            schema=[                    # The schema for the table
                bigquery.SchemaField(name="line", field_type="STRING", mode="REQUIRED", description ="The id of the line"),
                bigquery.SchemaField(name="LineWheelchairAccessible", field_type="STRING", mode="REQUIRED", description ="If the line ACCESSIBLE, NOTACCESSIBLE or UNKNOWN to wheelchairs"),
                bigquery.SchemaField(name="TransportType", field_type="STRING", mode="NULLABLE", description ="The transport type BUS METRO or TRAM"),
                bigquery.SchemaField(name="DestinationName50", field_type="STRING", mode="NULLABLE", description ="The name of the destination of the line"),
                bigquery.SchemaField(name="DataOwnerCode", field_type="STRING", mode="REQUIRED", description ="The code of the data owner"),
                bigquery.SchemaField(name="DestinationCode", field_type="STRING", mode="REQUIRED", description ="The code of the destination of the line"),
                bigquery.SchemaField(name="LinePublicNumber", field_type="STRING", mode="REQUIRED", description ="The line number used when communicated with travellers"),
                bigquery.SchemaField(name="LinePlanningNumber", field_type="STRING", mode="NULLABLE", description ="The planning number for the line"),
                bigquery.SchemaField(name="LineName", field_type="STRING", mode="NULLABLE", description ="The name of the line"),
                bigquery.SchemaField(name="LineDirection", field_type="STRING", mode="REQUIRED", description ="The direction of the line"),
                bigquery.SchemaField(name="execution_date", field_type="DATE", mode="REQUIRED", description ="The date at which the data was pulled from the API")
            ]
        )

    json_to_bq = PythonOperator(
        task_id='json_to_bq',
        python_callable=run_json_to_bq,
        provide_context=True,  # to pass the 'task_instance' argument
        retries=3,          # The number of times to retry the task if it fails
        retry_delay=timedelta(minutes=10)            # The delay between retries
    )

    end = DummyOperator(task_id = 'end')

ovapi_to_json >> json_to_bq >> end
