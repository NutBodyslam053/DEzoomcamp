import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f'curl -L {url} -o {csv_name}') # Windows
    # os.system(f'wget {url} -O {csv_name}') # Linux

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Import CSV file into Pandas Dataframe.
    df_iter = pd.read_csv(csv_name, dtype={'store_and_fwd_flag': 'str'}, iterator=True, chunksize=100000)
    df = next(df_iter)

    times, df_size = 0, 0
    t_start = time()

    # Transform columns into datetime format.
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Create a table with a specified columns.
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    # Add the initial chunk to the database.
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    t_end = time()
    times += t_end-t_start
    df_size += len(df)

    print('{:,} rows added to the database, elapsed time: {:.3f} second.'.format(df_size, times))

    # Add the remaining chunks to the database.
    for df in df_iter:
        t_start = time()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

        t_end = time()
        times += t_end-t_start
        df_size += len(df)

        print('{:,} rows added to the database, elapsed time: {:.3f} seconds.'.format(df_size, times))

    print('Complete!')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet data to Postgres database')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table where we will write the results to')
    parser.add_argument('--url', help='url of the file')
    
    args = parser.parse_args()
    main(args)


# Ex.) python ingest-data.py --user=root --password=root --host=localhost --port=5431 --db=postgres --table_name=yellow_taxi_data --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
