## 2_docker_sql
- Ingesting data into a PostgreSQL database running on Docker
    - Docker-compose: Generate a PostgreSQL database & PgAdmin4

## 3_prefect_gcp

### 00_prepare: Set up environments
- Local:
    - conda create -n `zoom` python=3.9
    - conda activate `zoom`
    - pip install -r requirements.txt
    - prefect orion start -> Go to dashboard at http://127.0.0.1:4200
- PostgreSQL:
    - Blocks -> add `SQLAlchemy Connector`
    - set up Block Name = "postgres-connector"
    - set up Driver -> SyncDriver = postgresql+psycopg2
    - set up Database = "ny_taxi", Username = "postgres", Password = "root", Host = "localhost", Port = 5432
- GCP:
    - Blocks -> add `GCP Credentials`
    - set up Block Name = "zoom-gcs-creds"
    - set up Service Account Info = <gcs_key.json>
    - Blocks -> add `GCS Bucket`
    - set up Block Name = "zoom-gcs"
    - set up Bucket = "dtc_data_lake_datatalksclub-376515"
    - set up Gcp Credentials -> add zoom-gcs-creds
- Docker:
    - Blocks -> add `Docker Container`
    - set up Block Name = "zoom"
    - set up Image = "nutbodyslam053/etl_prefect:zoom"
    - set up ImagePullPolicy = ALWAYS

### 01_start: PostgreSQL & Prefect
- Ingesting data into a PostgreSQL database running on local :: `Web -> PostgreSQL`
    - Main-flows:
        - Extract data from a data source
        - Transform data
        - Ingest data to a database
    - Sub-flow:
        - Print table name

### 02_gcp: Google Cloud Platform (GCP) & Prefect
- ETL workflow :: `Web -> Local -> GCS -> BigQuery`
    - Main-flows:
        - Fetch data from a data source
        - Clean data
        - Write data to a local repository
        - Upload data to GCS
        - Extract data from GCS
        - Transform data
        - Load data to BigQuery
### 03_deployments:
- Parameterizing Flow & Deployment with ETL Integration into GCS Workflow
    - Main-flows:
        - Loop through a set of months to perform a series of operations on the data for each month
    - Sub-flow:
        - Fetch data from a data source
        - Clean data
        - Write data to a local repository
        - Upload data to GCS