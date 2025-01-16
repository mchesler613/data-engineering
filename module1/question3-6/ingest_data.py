import argparse
import gzip
import os
import pandas as pd
import pp
import psycopg
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import requests

from pgpq import ArrowToPostgresBinaryEncoder
from urllib.parse import urlparse


DEFAULT_USER = "root"
DEFAULT_PW = "root"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "5432"
DEFAULT_DB = "ny_taxi"
DEFAULT_TABLE = "green_taxi"
DEFAULT_DATAFILE = "green_tripdata_2019-10.parquet"
DEFAULT_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    f"{DEFAULT_DATAFILE}"
)
LOCAL_PATH = "dataset/{datafile}"
DB_PATH = 'postgresql://{USER}:{PW}@{HOST}:{PORT}/{DB}'
TAXI_ZONE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/"
    "misc/taxi_zone_lookup.csv"
)


def get_data_filename(url: str) -> str:
    """
    Parse the url string and return the filename that
    ends with a .csv or .parquet
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    parts = path.split("/")
    return parts[-1]


def read_parquet_dataset_to_pf(url: str) -> pa.Table:
    """
    Read parquet dataset from url to write to local .parquet file
    and return a pyarrow.Table instance
    """
    # retrieve the parquet file from http source
    # and write to local parquet file
    response = requests.get(url)
    response.raise_for_status()
    data_file = get_data_filename(url)

    global LOCAL_PATH
    local_path = LOCAL_PATH.format(datafile=data_file)
    debug_print(f"local_path={local_path}")
    with open(local_path, "wb") as f:
        f.write(response.content)

    # retrieve the pyarrow.Table instance from local parquet file
    dataset = ds.dataset(local_path, format="parquet")
    pa_table = dataset.to_table()

    # detect null data types and remove it from pa_table
    # e.g. 2019 yellow taxi data has additional airport_fee
    # field with null type
    new_table = remove_null_types(pa_table)
    print(f'{new_table.num_rows} rows read')

    return new_table


def read_csv_dataset_to_pf(url) -> pa.Table:
    """
    Read CSV dataset from url to write to local .parquet file
    and return a pyarrow.Table instance
    """
    # get the .csv filename
    data_file = get_data_filename(url)

    # replace .csv extension to .parquet
    data_file = data_file.replace("csv", "parquet")
    print(data_file)

    global LOCAL_PATH
    local_path = LOCAL_PATH.format(datafile=data_file)
    debug_print(f"local_path={local_path}")

    # create a Pandas dataframe from url
    # if data_file is compressed, uncompress it
    if "gz" in data_file:
        with gzip.open(url) as file:
            df = pd.read_csv(file)
    else:
        df = pd.read_csv(url)

    # create a Pyarrow Table from dataframe
    arrow_table = pa.Table.from_pandas(df)

    print(f'{arrow_table.num_rows} rows read')

    # write table to parquet file
    pq.write_table(arrow_table, local_path)

    return arrow_table


def remove_null_types(
    arrow_table: pa.Table
) -> pa.Table:
    debug_print(f'arrow_table.schema.types {arrow_table.schema.types}')
    index_list = []
    for index, type in enumerate(arrow_table.schema.types):
        if type == pa.null():
            index_list.append(index)

    # remove null types from schema
    debug_print(f'index_list {index_list}')
    new_table = arrow_table
    for index in index_list:
        _ = arrow_table.schema.remove(index)
        new_table = arrow_table.remove_column(index)

    debug_print('new_table')
    debug_print(new_table)

    return new_table


def create_db_table_columns(
    connection,
    cursor,
    db_schema,
    table_name: str,
) -> None:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f'drop table {table_name}')
    cols = [
        f'"{col_name}" {col.data_type.ddl()}'
        for col_name, col in db_schema.columns
    ]
    debug_print(cols)
    sql = f"CREATE TABLE {table_name} ({','.join(cols)})"
    cursor.execute(sql)
    connection.commit()


def populate_db_table_rows(
    cursor,
    encoder,
    arrow_table: pa.Table,
    table_name: str,
) -> int:
    with cursor.copy(
        f"COPY {table_name} from STDIN WITH (FORMAT BINARY)"
    ) as copy:
        print(".", end="")
        copy.write(encoder.write_header())
        for batch in arrow_table.to_batches():
            print(".", end="")
            copy.write(encoder.write_batch(batch))
        print(".", end="")
        copy.write(encoder.finish())
        print(end="\n")

    cursor.execute(f"SELECT COUNT(*) from {table_name}")
    (number_of_rows,) = cursor.fetchone()
    print(f"{number_of_rows} rows ingested")
    return number_of_rows


def create_and_populate_db_table(
    db_path: str,
    arrow_table: pa.Table,
    table_name: str,
) -> int:
    """
    Create and populate database table from pyarrow table schema
    and return number of rows ingested
    Adapted from https://github.com/adriangb/pgpq
    """
    with psycopg.connect(db_path) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            encoder = ArrowToPostgresBinaryEncoder(arrow_table.schema)
            db_schema = encoder.schema()
            create_db_table_columns(connection, cursor, db_schema, table_name)
            rows_ingested = populate_db_table_rows(
                cursor, encoder, arrow_table, table_name
            )
    connection.close()
    return rows_ingested


def get_database_path(args: argparse.Namespace) -> str:
    print('Arguments passed:')
    print(args)

    db_path = DB_PATH.format(
        USER=args.user,
        PW=args.password,
        HOST=args.host,
        PORT=args.port,
        DB=args.db,
    )
    print('Database URI')
    print(db_path)
    return db_path


def ingest_parquet_data(
    db_path: str,
    url: str,
    table_name: str
) -> None:
    """
    Ingest Parquet data from url to Postgres database
    defined by db_path and table_name
    """
    print('Ingest Parquet Data from', url)
    arrow_table = read_parquet_dataset_to_pf(url)

    print('Populate Postgres Table')
    table_rows = create_and_populate_db_table(
        db_path, arrow_table, table_name
    )

    assert arrow_table.num_rows == table_rows


def ingest_csv_data(
    db_path: str,
    url: str,
    table_name: str
) -> None:
    """
    Ingest CSV data from url to Postgres database
    defined by db_path and table_name
    """
    print('Ingest CSV Data from', url)
    arrow_table = read_csv_dataset_to_pf(url)
    print('Populate Postgres Table')
    table_rows = create_and_populate_db_table(
        db_path, arrow_table, table_name
    )

    assert arrow_table.num_rows == table_rows


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Ingest parquet data from url to Postgres'
    )
    parser.add_argument(
        '--user', help='Postgres username', default=DEFAULT_USER
    )
    parser.add_argument(
        '--password', help='Postgres password', default=DEFAULT_PW
    )
    parser.add_argument(
        '--host', help='Postgres host name', default=DEFAULT_HOST
    )
    parser.add_argument(
        '--port', help='Postgres port number', default=DEFAULT_PORT
    )
    parser.add_argument(
        '--db', help='Postgres database name', default=DEFAULT_DB
    )
    parser.add_argument(
        '--table_name', help='Postgres table Name', default=DEFAULT_TABLE
    )
    parser.add_argument(
        '--url', help='URL of parquet file', default=DEFAULT_URL
    )
    input_args = parser.parse_args()
    return input_args


def debug_print(data: any) -> None:
    if os.getenv("DEBUG_PRINT") is None:
        return
    if isinstance(data, str):
        print(data)
    else:
        pp(data)


if __name__ == "__main__":
    args = parse_arguments()
    try:
        db_path = get_database_path(args)
        ingest_parquet_data(db_path, args.url, args.table_name)
        ingest_csv_data(db_path, TAXI_ZONE_URL, "taxi_zones")
    except Exception as error:
        print(error)
