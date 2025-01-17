# Data Engineering Module 1 Answers for Questions 3-6

## Table of Contents
Steps to follow:
1. [Setup development environment](#setup-development-environment)
2. [Build Docker container for Postgres and pgadmin](#build-docker-container-for-postgres-and-pgadmin)
3. [Ingest data via Python script](#Ingest-2019-NY-green-taxi-and-taxi-zones-data)
4. Ingest data via docker run
    - [Build Docker image for script via `Dockerfile`](#Build-a-Docker-image-based-on-Dockerfile)
    - [Run Docker image for script](#Ingest-Data-via-Docker)
5. [Check postgres database with `pgcli`](#Check-the-postgres-database-with-pgcli)
6. Answer homework questions 3 through 6
    - [Question 1](#Question-1)
    - [Question 2](#Question-2)
    - [Question 3](#Question-3)
    - [Question 4](#Question-4)
    - [Question 5](#Question-5)
    - [Question 6](#Question-6)

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

# Check the postgres database with pgcli
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

# Question 1

## Dockerfile

```
$ cat Dockerfile
FROM python:3.12.8

# specify work directory
WORKDIR /app

RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv

# Question 1 entrypoint is bash only
ENTRYPOINT [ "bash" ]
```

## build docker with docker build from Dockerfile

```
$ docker build -t h1:q1 .
[+] Building 8.3s (7/7) FINISHED                                                                    docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                0.0s
 => => transferring dockerfile: 469B                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.12.8                                                    0.5s
 => [internal] load .dockerignore                                                                                   0.0s
 => => transferring context: 2B                                                                                     0.0s
 => CACHED [1/3] FROM docker.io/library/python:3.12.8@sha256:251ef8e69b6ccdf3c7bf7effaa51179d59af35364dd9c86469142  0.0s
 => => resolve docker.io/library/python:3.12.8@sha256:251ef8e69b6ccdf3c7bf7effaa51179d59af35364dd9c86469142aa72a2c  0.0s
 => [2/3] WORKDIR /app                                                                                              0.0s
 => [3/3] RUN python -m venv /venv                                                                                  4.7s
 => exporting to image                                                                                              2.9s
 => => exporting layers                                                                                             1.5s
 => => exporting manifest sha256:c753894e17a7797f7d9d5bb2779e3e3c8028a50b7a0c4b53eb5def4d7c31b95c                   0.1s
 => => exporting config sha256:247f859408653c5b07ee0fc39da69fc404f4121b8b0c33017bbc20e9c90b5dea                     0.1s
 => => exporting attestation manifest sha256:22bf60b95d28a2455e0793642d60ad47851de31dab0476a2788944358667cad3       0.3s
 => => exporting manifest list sha256:17740e0a1cbd726df9ab5a228b10678489bb80e909258b18a98ce2e653ebf5c1              0.2s
 => => naming to docker.io/library/h1:q1                                                                            0.0s
 => => unpacking to docker.io/library/h1:q1```
```
## run docker with docker run --it

```
$ docker run -it h1:q1
root@8f9965d6afb3:/app# python --version
Python 3.12.8
root@8f9965d6afb3:/app# pip --version
pip 24.3.1 from /venv/lib/python3.12/site-packages/pip (python 3.12)
root@8f9965d6afb3:/app#
```
## Answer
Version of `pip` is `24.3.1`

# Question 2
## Content of `docker-compose.yaml`
```
$ cat docker-compose.yaml
services:
  db:
    container_name: postgres-2
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin-2
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8082:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

## docker compose up -d
```
$ docker compose up -d
[+] Running 2/2
 ✔ Container postgres-2  Running                                                   0.0s
 ✔ Container pgadmin-2   Started                                                   1.4s
```

## Access http://localhost:8082 on browser
Register a Postgres server with hostname `db` and port `5432`

![2025-01-17-12-46-27.jpg](https://i.postimg.cc/hGP7j8X4/2025-01-17-12-46-27.jpg)

## Answer
`db:5432`

# Question 3

## Build Dockerfile

```
docker build -t h1:q3 .
[+] Building 3.6s (15/15) FINISHED                                         docker:desktop-linux
 => [internal] load build definition from Dockerfile                                       0.0s
 => => transferring dockerfile: 510B                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.12.8                           0.6s
 => [internal] load .dockerignore                                                          0.0s
 => => transferring context: 2B                                                            0.0s
 => [ 1/10] FROM docker.io/library/python:3.12.8@sha256:044cfd88c6740313ae0de09e18d77a544  0.0s
 => => resolve docker.io/library/python:3.12.8@sha256:044cfd88c6740313ae0de09e18d77a54475  0.0s
 => [internal] load build context                                                          0.5s
 => => transferring context: 25.67MB                                                       0.5s
 => CACHED [ 2/10] RUN apt-get update && pip install poetry==2.0.0                         0.0s
 => CACHED [ 3/10] WORKDIR /app                                                            0.0s
 => CACHED [ 4/10] COPY ./README.md /app/README.md                                         0.0s
 => CACHED [ 5/10] COPY ./poetry.lock /app/poetry.lock                                     0.0s
 => CACHED [ 6/10] COPY ./pyproject.toml /app/pyproject.toml                               0.0s
 => CACHED [ 7/10] RUN python -m venv /venv                                                0.0s
 => CACHED [ 8/10] RUN poetry install --sync --no-root                                     0.0s
 => [ 9/10] COPY dataset /app/dataset                                                      0.3s
 => [10/10] COPY ingest_data.py /app/ingest_data.py                                        0.0s
 => exporting to image                                                                     2.0s
 => => exporting layers                                                                    1.5s
 => => exporting manifest sha256:d5881e592be333b39d30af980876d54d7312397e2e7238883cb8c21c  0.0s
 => => exporting config sha256:dd308b8eeecfec3e24db49a30d973409cc96414a397d77622e18604739  0.0s
 => => exporting attestation manifest sha256:05a9764975073b4b61b4a1c064b4ffc0885413d15404  0.0s
 => => exporting manifest list sha256:cc4c5ccea993f7919262ede63b8f317a2d6749fc46da94d7732  0.0s
 => => naming to docker.io/library/h1:q3                                                   0.0s
 => => unpacking to docker.io/library/h1:q3                                                0.4s
```

## Run Dockerfile

```
docker run -it --network=net-pgdata h1:q3 --host=postgres_service
Arguments passed:
Namespace(user='root', password='root', host='postgres_service', port='5432', db='ny_taxi', table_name='green_taxi', url='https://d37ci6vzurychx.cloudfront.net/trip-datagreen_tripdata_2019-10.parquet')
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
## Queries
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened 
- `up to 1 mile`?

```
root@localhost:ny_taxi> 
select count(*) from green_taxi 
where lpep_pickup_datetime>='2019-10-01 00:00:00' 
and lpep_pickup_datetime<'2019-11-01 00:00:00' 
and lpep_dropoff_datetime>='2019-10-01 00:00:00' 
and lpep_dropoff_datetime<'2019-11-01 00:00:00' 
and trip_distance<=1
;
+--------+
| count  |
|--------|
| 104802 |
+--------+

```
- `In between 1 (exclusive) and 3 miles (inclusive)`
```
root@localhost:ny_taxi> 
select count(*) from green_taxi 
where lpep_pickup_datetime>='2019-10-01 00:00:00' 
and lpep_pickup_datetime<'2019-11-01 00:00:00' 
and lpep_dropoff_datetime>='2019-10-01 00:00:00' 
and lpep_dropoff_datetime<'2019-11-01 00:00:00' 
and trip_distance > 1 and trip_distance <= 3
;
+--------+
| count  |
|--------|
| 198924 |
+--------+
```

- `In between 3 (exclusive) and 7 miles (inclusive)`
```
root@localhost:ny_taxi> 
select count(*) from green_taxi 
where lpep_pickup_datetime>='2019-10-01 00:00:00' 
and lpep_pickup_datetime<'2019-11-01 00:00:00' 
and lpep_dropoff_datetime>='2019-10-01 00:00:00' 
and lpep_dropoff_datetime<'2019-11-01 00:00:00' 
and trip_distance > 3 and trip_distance <= 7
;
+--------+
| count  |
|--------|
| 109603 |
+--------+
```
- `In between 7 (exclusive) and 10 miles (inclusive)`
```
root@localhost:ny_taxi> 
select count(*) from green_taxi 
where lpep_pickup_datetime>='2019-10-01 00:00:00' 
and lpep_pickup_datetime<'2019-11-01 00:00:00' 
and lpep_dropoff_datetime>='2019-10-01 00:00:00' 
and lpep_dropoff_datetime<'2019-11-01 00:00:00' 
and trip_distance > 7 and trip_distance <= 10
;
+-------+
| count |
|-------|
| 27678 |
+-------+
```
- `Over 10 miles`
```
root@localhost:ny_taxi> 
select count(*) from green_taxi 
where lpep_pickup_datetime>='2019-10-01 00:00:00' 
and lpep_pickup_datetime<'2019-11-01 00:00:00' 
and lpep_dropoff_datetime>='2019-10-01 00:00:00' 
and lpep_dropoff_datetime<'2019-11-01 00:00:00' 
and trip_distance > 10
;
+-------+
| count |
|-------|
| 35189 |
+-------+
```
## Answer
`104,802; 198,924; 109,603; 27,678; 35,189`

# Question 4
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance.

```
root@localhost:ny_taxi> 
select lpep_pickup_datetime, trip_distance 
from green_taxi 
order by trip_distance desc 
limit 3
+----------------------+---------------+
| lpep_pickup_datetime | trip_distance |
|----------------------+---------------|
| 2019-10-31 23:23:41  | 515.89        |
| 2019-10-11 20:34:21  | 95.78         |
| 2019-10-26 03:02:39  | 91.56         |
+----------------------+---------------+
```

## Answer 
`2019-10-31`

# Question 5
Which were the top pickup locations with over 13,000 in `total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.

	-East Harlem North, East Harlem South, Morningside Heights
	-East Harlem North, Morningside Heights
	-Morningside Heights, Astoria Park, East Harlem South
	-Bedford, East Harlem North, Astoria Park

```
root@localhost:ny_taxi> 
select "Zone" from taxi_zones where "LocationID" in (
 	select "PULocationID" from green_taxi
  	where lpep_pickup_datetime>='2019-10-18 00:00:00' 
	and lpep_pickup_datetime<'2019-10-19 00:00:00'
  	group by "PULocationID"
 	 having sum(total_amount) > 13000
 	 order by sum(total_amount) desc limit 3
  );
+---------------------+
| Zone                |
|---------------------|
| East Harlem North   |
| East Harlem South   |
| Morningside Heights |
+---------------------+
SELECT 3
Time: 0.073s
```
## Answer
`East Harlem North, East Harlem South, Morningside Heights`

# Question 6
For the passengers picked up in October 2019 in the zone name "East Harlem North", which was the drop off zone that had the largest tip?

```
root@localhost:ny_taxi>  select "DOLocationID", tip_amount  from green_taxi
  where lpep_pickup_datetime>='2019-10-01 00:00:00'
  and lpep_pickup_datetime < '2019-11-01 00:00:00'
  and "PULocationID" in (
      select "LocationID" from taxi_zones where "Zone"='East Harlem North'
  )
   group by "DOLocationID", tip_amount
   order by tip_amount desc limit 3;
+--------------+------------+
| DOLocationID | tip_amount |
|--------------+------------|
| 132          | 87.3       |
| 263          | 80.88      |
| 74           | 40.0       |
+--------------+------------+

root@localhost:ny_taxi> select "Zone" from taxi_zones where "LocationID"=132;
+-------------+
| Zone        |
|-------------|
| JFK Airport |
+-------------+
SELECT 1
Time: 0.006s
```
## Answer
`JFK Airport`