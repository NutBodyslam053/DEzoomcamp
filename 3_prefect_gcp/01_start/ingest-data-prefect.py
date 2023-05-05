import os
import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector

@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # Retrieve data from the internet.
    os.system(f'curl -L {url} -o {csv_name}')

    # Import CSV file into Pandas Dataframe.
    df_iter = pd.read_csv(csv_name, dtype={'store_and_fwd_flag': 'str'}, iterator=True, chunksize=100000)
    df = next(df_iter)

    # Transform columns into datetime format.
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    return df

@task(log_prints=True)
def transform_data(df):
    # Remove missing passenger from the dataframe.
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")

    return df

@task(log_prints=True, retries=3)
def ingest_data(table_name, df):
    # Establish a connection to the PostgreSQL block.
    connection_block = SqlAlchemyConnector.load("postgres-connector")

    with connection_block.get_connection(begin=False) as engine:
        # Create a table with a specified columns.
        df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        # Add the initial chunk to the database.
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging Subflow for: {table_name}")

@flow(name="Ingest Flow")
def main_flow(table_name: str="yellow_taxi_trips"):
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

    # Subflow
    log_subflow(table_name)
    
    # Tasks
    raw_data = extract_data(csv_url)
    data = transform_data(raw_data)
    ingest_data(table_name, data)

if __name__=='__main__':
    main_flow(table_name="yellow_taxi_trips")