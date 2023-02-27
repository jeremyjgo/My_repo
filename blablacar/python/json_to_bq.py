import os
from google.cloud import bigquery
from google.cloud.exceptions import NotFound


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bq_conn.json'


class BigQueryTable:
    """
    A class for creating and managing BigQuery tables.

    Attributes:
        dataset_id (str): The ID of the dataset containing the table.
        table_id (str): The ID of the table.
        schema (list): A list of bigquery.SchemaField objects defining the table schema.
    """
    def __init__(self, dataset_id, table_id, schema):
        """
        Initializes a BigQueryTable object.

        Args:
            dataset_id (str): The ID of the dataset containing the table.
            table_id (str): The ID of the table.
            schema (list): A list of bigquery.SchemaField objects defining the table schema.
        """
        self.client = bigquery.Client()
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.schema = schema
        self.table_ref = self.client.dataset(self.dataset_id).table(self.table_id)

    def create_table_if_not_exists(self, partition_field=None, partition_type=None, clustering_fields=None, expiration_ms=None):
        """
        Creates the table if it does not already exist.

        Args:
            partition_field (str, optional): The name of the field to partition the table by. Defaults to None.
            partition_type (str, optional): The type of partitioning to use, such as 'day' or 'hour'. Defaults to None.
            clustering_fields (list, optional): A list of field names to cluster the table by. Defaults to None.
            expiration_ms (int, optional): The duration for which the partitioned data is retained, in milliseconds. Defaults to None.
        """
        table = bigquery.Table(self.table_ref, schema=self.schema)
        # Checks that the partition field is present in the schema
        if partition_field not in [field.name for field in self.schema]:
            raise ValueError(f"Partition field '{partition_field}' not found in schema.")
        # Checks that the clustering fields are in the schema
        if clustering_fields:
            for field in clustering_fields:
                if field not in [field.name for field in self.schema]:
                    raise ValueError(f"Clustering field {field} is not in the table schema.")

        # Checks that if the table already exists and creates it if needed.
        try:
            self.client.get_table(self.table_ref)
            print(f"Table {self.table_id} already exists in {self.dataset_id}.")
        except NotFound:
            if partition_field and partition_type:
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=partition_type.upper(),
                    field=partition_field,
                    expiration_ms = expiration_ms
                )
            if clustering_fields:
                table.clustering_fields = clustering_fields
                
            table = self.client.create_table(table)
            print(f"Table {self.table_id} created in {self.dataset_id}.")

    def json_to_big_query(self, json_data):
        """
        Loads JSON data into a BigQuery table.

        Args:
            json_data (List[Dict[str, Any]]): The data to load, as a list of dictionaries, newline delimited.
            dataset_id (str): The ID of the dataset in BigQuery to load the data into.
            table_id (str): The ID of the table in the dataset to load the data into.
            schema (List[bigquery.SchemaField]): The schema of the data.

        Raises:
            Exception: If there are any errors while loading the data into BigQuery.

        Returns:
            None.
        """
        # Creates the table if it does not exist
        self.create_table_if_not_exists()

        # Create BigQuery client and table reference
        client = bigquery.Client()
        table_ref = client.dataset(dataset_id).table(table_id)

        # Get table information and partition field
        table = self.client.get_table(table_ref)
        partition_field = table.time_partitioning.field if table.time_partitioning else None

        # Delete partition if it exists
        if partition_field:
            query = f"DELETE FROM `{dataset_id}.{table_id}` WHERE {partition_field} = DATE('{json_data[0][partition_field]}')"
            job_config = bigquery.QueryJobConfig()
            job_config.use_legacy_sql = False
            delete_job = self.client.query(query, job_config=job_config)
            delete_job.result()

        # Load data into BigQuery table
        job_config = bigquery.LoadJobConfig()
        job_config.schema = self.schema
        job = client.load_table_from_json(json_data, table_ref, job_config=job_config)
        job.result()

        # Check for errors and raise exception if necessary
        if job.errors:
            error_msg = "Errors occurred while loading data into BigQuery:"
            for error in job.errors:
                error_msg += f"\n{error['message']}"
            raise Exception(error_msg)

        # Print success message
        print(f"Loaded {job.output_rows} rows into {dataset_id}.{table_id}.")



