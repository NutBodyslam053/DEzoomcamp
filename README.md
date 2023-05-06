## 2_docker_sql
- Ingesting data into a PostgreSQL database running on Docker :: `Web -> PostgreSQL`

## 3_prefect_gcp

### 00_setup
- Google Cloud Platform (GCP):
    - Google Cloud Storage (GCS):
        - Cloud Storage -> create `Buckets` = "dtc_data_lake_datatalksclub-376515"
        - IAM & Admin -> create `Service Accounts` = "zoom-de-service-acct" 
        - set up Grant this service account.. -> add Role = ["BigQuery Admin", "Storage Admin"]
        - generate `KEYS` -> create new key = JSON (<gcs_key.json> will be automatically downloaded)
    - BigQuery:
        - Explorer -> add data -> choose Google Cloud Storage
        - set up Source -> browse file from GCS bucket, File format = "Parquet"
        - set up Destination -> Dataset = "dezoomcamp", Table = "rides"
        - QUERY Editor -> DELETE FROM <project_id.dataset_name.table_name> WHERE TRUE; (clear up the data)
- Local:
    - create `data/yellow` folder
    - conda create -n `zoom` python=3.9
    - conda activate `zoom`
    - pip install -r requirements.txt
    - prefect orion start -> go to dashboard at http://127.0.0.1:4200
- Prefect:
    - PostgreSQL:
        - Blocks -> add `SQLAlchemy Connector`
        - set up Block Name = "postgres-connector"
        - set up Driver -> SyncDriver = postgresql+psycopg2
        - set up Database = "ny_taxi", Username = "postgres", Password = "root", Host = "localhost", Port = 5432
    - Google Cloud Platform (GCP):
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
        - set up Image = "nutbodyslam053/etl_prefect:zoom" (Image name from Docker Hub)
        - set up ImagePullPolicy = ALWAYS

### 01_start
- Ingesting data into a PostgreSQL database running on Local :: `Web -> PostgreSQL`
    - Main-flows:
        - Extract data from a data source
        - Transform data
        - Ingest data to a database
    - Sub-flow:
        - Print table name

### 02_gcp
- ETL workflow :: `Web -> Local -> GCS -> BigQuery`
    - Main-flows:
        - Fetch data from a data source
        - Clean data
        - Write data to a local repository
        - Upload data to GCS
        - Extract data from GCS
        - Transform data
        - Load data to BigQuery

### 03_deployments
- Parameterizing Flow & Deployments
    - Using CLI
    ```Python
    # Build a flow code file named `xxx-deployment.yaml`
    prefect deployment build 3_prefect_gcp\03_deployments\parameterized_flow.py:etl_parent_flow -n "Parameterized_ETL"

    # Upload the flow code file into Prefect web-UI/Deployments
    prefect deployment apply "etl_parent_flow-deployment.yaml"

    # Start an agent Work Queue to exceute flow runs from Deployments (open another terminal)
    prefect agent start --work-queue "default"  

    # Run the flows on Prefect web-UI
    prefect deployment run "etl-parent-flow/Parameterized_ETL" -p "months=[1,2,3]"

    # Build & Apply the flows-script into Prefect web-UI/Deployments with crontab
    prefect deployment build 3_prefect_gcp\03_deployments\parameterized_flow.py:etl_parent_flow -n "etl" --cron "0 0 * * *" -a
    ```
    - Using Docker Image
    ```Python
    # Make a Docker file & Generate a Docker image
    docker image build -t nutbodyslam053/etl_prefect:zoom .

    # Push the image into Docker Hub, then connect a Docker Container Block on Prefect web-UI/Blocks
    docker push nutbodyslam053/etl_prefect:zoom

    # Make sure prefect API is set correctly, to make docker able to talk to the orion server
    prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"

    # Make a docker_deploy.py, import etl_parent_flow from parameterized_flow.py, and execute to upload the flow code file into Prefect web-UI/Deployments
    python 3_prefect_gcp\03_deployments\docker_deploy.py

    # Start an agent Work Queue to exceute flow runs from Deployments (open another terminal)
    prefect agent start -q "default"

    # Run the flows on Prefect web-UI
    prefect deployment run "etl-parent-flow/docker-flow" -p "months=[1,2,3]"
    ```