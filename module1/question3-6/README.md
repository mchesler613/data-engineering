# Data Engineering Module 1 Answers for Questions 3-6

Steps to follow:
1. [Setup development environment](#setup-development-environment)
2. [Build Docker container for postgres and pgadmin](#build-docker-container-for-postgres-and-pgadmin)
3. [Ingest data via python script](#Ingest-2019 -NY-green-taxi-and-taxi-zones-data)
4. Ingest data via docker run
    - [Build Docker image for script via `Dockerfile`](#Build-a-Docker-image-based-on-Dockerfile)
    - [Run Docker image for script](#Ingest-Data-via-Docker)
5. [Check postgres database with `pgcli`](#Check-the-postgres-database-with-`pgcli`)
6. Answer homework questions 3 through 6


# Setup development environment
This directory is maintained by [poetry](https://python-poetry.org) and [pyenv](https://github.com/pyenv/pyenv-installer). To create a virtual environment, do the following:

```
pyenv shell 3.12
poetry env use 3.12
source $(poetry env info --path)/bin/activate
poetry install
```

# Build Docker container for postgres and pgadmin

Create a `docker-compose.yaml` file
```
docker compose up -d
```

# Ingest 2019 NY green taxi and taxi zones data
Running the python script, `ingest_data.py`, will ingest:

- a parquet file with options (see below)
- a csv file containing taxi zones data

into the Postgres database built within Docker above.

To see the options for this script:
```
$ python ingest_data.py --help
usage: ingest_data.py [-h] [--user USER] [--password PASSWORD] [--host HOST]
                      [--port PORT] [--db DB] [--table_name TABLE_NAME] [--url URL]

Ingest parquet data from url to Postgres

options:
  -h, --help            show this help message and exit
  --user USER           Postgres username
  --password PASSWORD   Postgres password
  --host HOST           Postgres host name
  --port PORT           Postgres port number
  --db DB               Postgres database name
  --table_name TABLE_NAME
                        Postgres table Name
  --url URL             URL of parquet file
```

Running the script without passing any arguments will use the default values specified in the script.

```
python ingest_data.py
Arguments passed:
Namespace(user='root', password='root', host='localhost', port='5432', db='ny_taxi', table_name='green_taxi', url='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet')
Database URI
postgresql://root:root@localhost:5432/ny_taxi
Ingest Parquet Data from https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet
476386 rows read
Populate Postgres Table
drop table green_taxi
......
476386 rows ingested
Ingest CSV Data from https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
taxi_zone_lookup.parquet
265 rows read
Populate Postgres Table
drop table taxi_zones
...
265 rows ingested
```

# Build a Docker image based on Dockerfile
Run `docker build -t module1:question3 .`

```
$ docker build -t module1:question3 .
[+] Building 55.6s (15/15) FINISHED                                docker:desktop-linux
 => [internal] load build definition from Dockerfile                               0.0s
 => => transferring dockerfile: 510B                                               0.0s
 => [internal] load metadata for docker.io/library/python:3.12.8                   0.7s
 => [internal] load .dockerignore                                                  0.0s
 => => transferring context: 2B                                                    0.0s
 => [ 1/10] FROM docker.io/library/python:3.12.8@sha256:5893362478144406ee0771bd9  0.0s
 => => resolve docker.io/library/python:3.12.8@sha256:5893362478144406ee0771bd9c3  0.0s
 => [internal] load build context                                                  1.5s
 => => transferring context: 36.85MB                                               1.5s
 => CACHED [ 2/10] RUN apt-get update && pip install poetry==2.0.0                 0.0s
 => CACHED [ 3/10] WORKDIR /app                                                    0.0s
 => [ 4/10] COPY ./README.md /app/README.md                                        0.1s
 => [ 5/10] COPY ./poetry.lock /app/poetry.lock                                    0.0s
 => [ 6/10] COPY ./pyproject.toml /app/pyproject.toml                              0.0s
 => [ 7/10] RUN python -m venv /venv                                               5.2s
 => [ 8/10] RUN poetry install --sync --no-root                                   18.1s
 => [ 9/10] COPY dataset /app/dataset                                              0.4s
 => [10/10] COPY ingest_data.py /app/ingest_data.py                                0.0s
 => exporting to image                                                            29.1s
 => => exporting layers                                                           20.0s
 => => exporting manifest sha256:77f1ad2b09bc0b401617266a0070229d1fd5bd48da040d1a  0.0s
 => => exporting config sha256:76e8ad95ce1bdcfaa4428f64b984be6365b7bc0f2a8932e7ad  0.0s
 => => exporting attestation manifest sha256:6b084440f090590477b17dfcfdf5203a6234  0.0s
 => => exporting manifest list sha256:314689f0ab15a7d981afddb2e86f3d9fffaf8d439d4  0.0s
 => => naming to docker.io/library/module1:question3                               0.0s
 => => unpacking to docker.io/library/module1:question3                            9.1s
```

# Ingest Data via Docker
`docker run -it --network=net-pgdata h1:q3 --host=postgres_service`

```
$ docker run -it --network=net-pgdata h1:q3 --host=postgres_service
Arguments passed:
Namespace(user='root', password='root', host='postgres_service', port='5432', db='ny_taxi', table_name='green_taxi', url='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet')
Database URI
postgresql://root:root@postgres_service:5432/ny_taxi
Ingest Parquet Data from https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet
476386 rows read
Populate Postgres Table
drop table green_taxi
......
476386 rows ingested
Ingest CSV Data from https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
taxi_zone_lookup.parquet
265 rows read
Populate Postgres Table
drop table taxi_zones
...
265 rows ingested
```

# Check the postgres database with `pgcli`
```
root@localhost:ny_taxi> select count(*) from green_taxi;
+--------+
| count  |
|--------|
| 476386 |
+--------+
SELECT 1
Time: 0.086s
root@localhost:ny_taxi> select count(*) from taxi_zones;
+-------+
| count |
|-------|
| 265   |
+-------+
SELECT 1
Time: 0.007s
```
