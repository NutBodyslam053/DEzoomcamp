## 2_docker_sql
- Ingesting data into a PostgreSQL database running on Docker
    - Docker-compose:
        - Create a PostgreSQL database & PgAdmin4

## 3_prefect_gcp
- 00_prepare environments
    - conda create -n zoom python=3.9
    - conda activate zoom
    - pip install -r requirements.txt
    - prefect orion start
    - Go to Prefect dashboard at http://127.0.0.1:4200
    - Blocks -> add SQLAlchemy Connector
    - set up Block Name = "postgres-connector"
    - set up Driver -> SyncDriver = postgresql+psycopg2
    - set up Database = "ny_taxi", Username = "postgres", Password = "root", Host = "localhost", Port = 5432
    - python ingest-data-prefect.py

- 01_start: Using Prefect
    - Ingesting data into a PostgreSQL database running on local
        - Main-flows:
            - Extract data
            - Transform data
            - Ingest data
        - Sub-flow:
            - Print table name

- 02_gcp: Google Cloud Platform (GCP) & Prefect
    - ELT: Data source [Web] -> Data Lake [Google Cloud Storage; GCS]
        - Main-flows:
            - Fetch data from a data source
            - Clean data
            - Write data to a local repository
            - Upload data to GCS
    - ETL: Data Lake [Google Cloud Storage; GCS] -> Data Warehouse [BigQuery]
        - Main-flows:
            - Extract data from GCS
            - Transform data
            - Load data to BigQuery
    - Parameterizing Flow & Deployment with ETL Integration into GCS Workflow
        - Main-flows:
            - Loop through a set of months to perform a series of operations on the data for each month
        - Sub-flow:
            - Fetch data from a data source
            - Clean data
            - Write data to a local repository
            - Upload data to GCS