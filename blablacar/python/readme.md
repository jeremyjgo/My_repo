General Observations:

No additional action are needed to execute the code. The files can be uploaded as they are to the code-base and the DAG to a
Airflow. It just needs to be turned on so that the CRON scheduling is enabled.

During the case study, I tried to use Object Oriented Programming as much as possible,
so that it could (theoratically) be added to a more complex production environnement.



Limitations:

As the API doesn't provide a date information, the data returned is always the data available at the time of the call. Therefore there doesn't seem to be a way a getting data from last year for example, for a potential backfill, if needed.

Columns are not renamed to keep the data as it comes from the API.

I my code, Big Query credentials are specified within a json file. 
However, I assume that in a production environment, a service account will be used and credentials will be kept in a separate location.
