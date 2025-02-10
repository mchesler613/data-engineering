# Data Engineering DLT Workshop Answers for Questions 1-4

## Preparatory Work

- use `poetry` and `pyenv` to create virtual environment
```
$ pyenv shell 3.12
$ poetry env use 3.12
$ source $(poetry env info --path)/bin/activate
```

- run `poetry install` to install dependencies from `poetry.lock` file

## Question 1

Question 1: dlt Version
Install dlt:
!pip install dlt[duckdb]
Or choose a different bracket—bigquery, redshift, etc.—if you prefer another primary destination. For this assignment, we’ll still do a quick test with DuckDB.

Check the version:
!dlt --version
or:

import dlt
print("dlt version:", dlt.__version__)
Answer:

Provide the version you see in the output.

```
$ dlt --version
dlt 1.6.1
```

## Question 2

Define & Run the Pipeline (NYC Taxi API)

How many tables were created?

```
$ dlt pipeline ny_taxi_pipeline trace
Found pipeline ny_taxi_pipeline in /Users/merilynchesler/.dlt/pipelines
Run started at 2025-02-10 21:06:59.370834+00:00 and COMPLETED in 24.95 seconds with 4 steps.
Step extract COMPLETED in 22.18 seconds.

Load package 1739221619.557778 is EXTRACTED and NOT YET LOADED to the destination and contains no failed jobs

Step normalize COMPLETED in 1.28 seconds.
Normalized data for the following tables:
- taxi_rides: 10000 row(s)
- _dlt_pipeline_state: 1 row(s)          <===  2 tables

Load package 1739221619.557778 is NORMALIZED and NOT YET LOADED to the destination and contains no failed jobs

Step load COMPLETED in 1.32 seconds.
Pipeline ny_taxi_pipeline load step completed in 1.29 seconds
1 load package(s) were loaded to destination duckdb and into dataset ny_taxi_data
The duckdb destination used duckdb:////Users/merilynchesler/data-engineering/workshop/ny_taxi_pipeline.duckdb location to store data
Load package 1739221619.557778 is LOADED and contains no failed jobs

Step run COMPLETED in 24.95 seconds.
Pipeline ny_taxi_pipeline load step completed in 1.29 seconds
1 load package(s) were loaded to destination duckdb and into dataset ny_taxi_data
The duckdb destination used duckdb:////Users/merilynchesler/data-engineering/workshop/ny_taxi_pipeline.duckdb location to store data
Load package 1739221619.557778 is LOADED and contains no failed jobs

```
Running `dlt pipeline ny_taxi_pipeline trace` shows 2 tables were created:
Normalized data for the following tables:
- taxi_rides: 10000 row(s)
- _dlt_pipeline_state: 1 row(s) 


## Question 3
Question 3: Explore the loaded data
Inspect the table ride:

df = pipeline.dataset(dataset_type="default").rides.df()
What is the total number of records extracted?

```
$ python pipeline.py
Pipeline ny_taxi_pipeline load step completed in 1.29 seconds
1 load package(s) were loaded to destination duckdb and into dataset ny_taxi_data
The duckdb destination used duckdb:////Users/merilynchesler/data-engineering/workshop/ny_taxi_pipeline.duckdb location to store data
Load package 1739221619.557778 is LOADED and contains no failed jobs
        end_lat    end_lon  ...         _dlt_id  store_and_forward
0     40.742963 -73.980072  ...  T4+L4+CEzZagDA                NaN
1     40.740187 -74.005698  ...  9lDqChQLIi/IGQ                NaN
2     40.718043 -74.004745  ...  p1afdhfNWixa8A                NaN
3     40.739637 -73.985233  ...  b/8D9PvVbAtvmA                NaN
4     40.730032 -73.852693  ...  iGNrTeZBuAEFsg                NaN
...         ...        ...  ...             ...                ...
9995  40.783522 -73.970690  ...  xd7wBLs5MJrnAg                NaN
9996  40.777200 -73.964197  ...  Y3SIDUXPFUjzgA                NaN
9997  40.780172 -73.957617  ...  XIspiMQtOkhokw                NaN
9998  40.777342 -73.957242  ...  LjxeD2ARKYp+rg                NaN
9999  40.757122 -73.986293  ...  WE3OOxpzp0vo+Q                NaN

[10000 rows x 18 columns]
```

Dataframe shows 10,000 rows.

## Question 4

Trip Duration Analysis
Run the SQL query below to:

Calculate the average trip duration in minutes.
```
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM taxi_rides;
            """
        )
    # Prints column values of the first row
    print(res)
```
What is the average trip duration?

Running this query in duckdb DLT Dashboard:
```
SELECT
        AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time)) as average_trip
        FROM taxi_rides
```

returns `12.3049` minutes

[![2025-02-10-17-10-13.jpg](https://i.postimg.cc/nV7x4q67/2025-02-10-17-10-13.jpg)](https://postimg.cc/grY1dLck)