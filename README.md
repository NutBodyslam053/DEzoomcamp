## 2_docker_sql
- Ingesting data into a PostgreSQL database running on Docker
    - Docker-compose:
        - Create a PostgreSQL database & PgAdmin4

## 3_prefect_gcp
- 01_start - Using Prefect
    - Ingesting data into a PostgreSQL database running on local
        - Main-flows:
            - Extract data
            - Transform data
            - Ingest data
        - Sub-flow:
            - Print table name
- 02_gcp - Google Cloud Platform (GCP) & Prefect
    - ELT: Data source -> Data Lake, Google Cloud Storage (GCS)
        - Main-flows:
            - Fetch data from a data source
            - Clean data
            - Write data to a local repository
            - Upload data to GCS
    - ETL: Data Lake, Google Cloud Storage (GCS) -> Data Warehouse, BigQuery
        - Main-flows:
            - Extract data from GCS
            - Transform data
            - Load data to BigQuery