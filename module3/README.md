# Data Engineering Module 3 Answers for Questions 1-9

## Preparatory Work

- use `poetry` and `pyenv` to create virtual environment
```
$ pyenv shell 3.12
$ poetry env use 3.12
$ source $(poetry env info --path)/bin/activate
```

- run `poetry install` to install dependencies from `poetry.lock` file

### script to upload parquet from NY Taxi directly to GCS
- run Python script, `upload_parquet_to_gcs.py` to load parquet files directly from NY Taxi folder to GCS

```
$ python upload_parquet_to_gcs.py
File yellow_tripdata_2024-01.parquet uploaded successfully to gs://merilyn_ny_taxi/yellow_tripdata_2024-01.parquet!
File yellow_tripdata_2024-02.parquet uploaded successfully to gs://merilyn_ny_taxi/yellow_tripdata_2024-02.parquet!
File yellow_tripdata_2024-03.parquet uploaded successfully to gs://merilyn_ny_taxi/yellow_tripdata_2024-03.parquet!
File yellow_tripdata_2024-04.parquet uploaded successfully to gs://merilyn_ny_taxi/yellow_tripdata_2024-04.parquet!
File yellow_tripdata_2024-05.parquet uploaded successfully to gs://merilyn_ny_taxi/yellow_tripdata_2024-05.parquet!
File yellow_tripdata_2024-06.parquet uploaded successfully to gs://merilyn_ny_taxi/yellow_tripdata_2024-06.parquet!
```
- verify that parquet files are loaded on GCS
```
$ gcloud storage ls -l gs://merilyn_ny_taxi/ | grep 2024
  49961641  2025-02-05T00:08:36Z  gs://merilyn_ny_taxi/yellow_tripdata_2024-01.parquet
  50349284  2025-02-05T00:08:55Z  gs://merilyn_ny_taxi/yellow_tripdata_2024-02.parquet
  60078280  2025-02-05T00:09:19Z  gs://merilyn_ny_taxi/yellow_tripdata_2024-03.parquet
  59133625  2025-02-05T00:09:41Z  gs://merilyn_ny_taxi/yellow_tripdata_2024-04.parquet
  62553128  2025-02-05T00:10:04Z  gs://merilyn_ny_taxi/yellow_tripdata_2024-05.parquet
  59859922  2025-02-05T00:10:27Z  gs://merilyn_ny_taxi/yellow_tripdata_2024-06.parquet
```

### create yellow_tripdata external table in GBQ from GCS

- create an external table referring to gcs path

```
create or replace external table silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata
options (
  format = 'PARQUET',
  uris = ['gs://merilyn_ny_taxi/yellow_tripdata_2024-*.parquet']
)
```

# Question 1: What is count of records for the 2024 Yellow Taxi Data?

```
65,623
840,402
20,332,093			 <==
85,431,289
```

```
select count(*) from silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata

20332093
```

- Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).

```
create or replace table silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata_non_partitioned as
select * from silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata
```

# Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```
18.82 MB for the External Table and 47.60 MB for the Materialized Table
0 MB for the External Table and 155.12 MB for the Materialized Table           <=== 
2.14 GB for the External Table and 0MB for the Materialized Table
0 MB for the External Table and 0MB for the Materialized Table
```

- materialized table
[![2025-02-04-20-57-56.jpg](https://i.postimg.cc/YCgHNqGh/2025-02-04-20-57-56.jpg)](https://postimg.cc/1892sSKQ)
- external table
[![2025-02-04-20-58-35.jpg](https://i.postimg.cc/ncNxQQLy/2025-02-04-20-58-35.jpg)](https://postimg.cc/GHPVWtGK)


# Question 3:
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?

```
BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.             <===
BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed
```

- PULocationID
[![2025-02-04-21-06-05.jpg](https://i.postimg.cc/jjDZnv8T/2025-02-04-21-06-05.jpg)](https://postimg.cc/f3hx67nq)
- PULocationID, DOLocationID
[![2025-02-04-21-06-33.jpg](https://i.postimg.cc/R02G7f8H/2025-02-04-21-06-33.jpg)](https://postimg.cc/SX7WqXmS)


# Question 4:
How many records have a fare_amount of 0?

```
128,210
546,578
20,188,016
8,333             <===
```

```
SELECT count(*) FROM `silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata_non_partitioned` where fare_amount = 0

8333
```

# Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_timedate and order the results by VendorID (Create a new table with this strategy)

```
Partition by tpep_dropoff_timedate and Cluster on VendorID                    <===
Cluster on by tpep_dropoff_timedate and Cluster on VendorID
Cluster on tpep_dropoff_timedate Partition by VendorID
Partition by tpep_dropoff_timedate and Partition by VendorID
```

# Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 03/01/2024 and 03/15/2024 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

Choose the answer which most closely matches.

```
12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
310.24 MB for non-partitioned table and 26.84 MB for the partitioned table             <===
5.87 MB for non-partitioned table and 0 MB for the partitioned table
310.31 MB for non-partitioned table and 285.64 MB for the partitioned table
```

```
create or replace table silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata_partitioned
partition by
  DATE(tpep_dropoff_timedate) as
select * from silent-blade-447917-q2.merilyn_ny_taxi.external_yellow_tripdata
```

- non-partitioned query
[![2025-02-04-21-48-15.jpg](https://i.postimg.cc/y8GJ1j9R/2025-02-04-21-48-15.jpg)](https://postimg.cc/CRjMJjcM)

- partitioned query
[![2025-02-04-21-52-06.jpg](https://i.postimg.cc/RZh6xy39/2025-02-04-21-52-06.jpg)](https://postimg.cc/k2rXxjFh)


# Question 7:
Where is the data stored in the External Table you created?

```
Big Query
Container Registry
GCP Bucket        <===
Big Table
```

[![2025-02-04-22-35-57.jpg](https://i.postimg.cc/YSCqcWjP/2025-02-04-22-35-57.jpg)](https://postimg.cc/FYwQ31yb)


# Question 8:
It is best practice in Big Query to always cluster your data:

```
True
False        <====
```

| **Scenario**                                         | **Use Clustering?** |
|------------------------------------------------------|---------------------|
| Query filters on **high-cardinality column**        | ✅ Yes |
| Large dataset (Several GB+ in size)                 | ✅ Yes |
| Already partitioned but queries filter within partitions | ✅ Yes |
| Small table (Few MBs)                                | ❌ No |
| Queries scan the whole table frequently             | ❌ No |
| Frequent updates or inserts                         | ❌ No |


(Bonus: Not worth points) Question 9:
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

0 bytes

[![2025-02-04-22-25-15.jpg](https://i.postimg.cc/Sxqxr54k/2025-02-04-22-25-15.jpg)](https://postimg.cc/rKnTyfzP)

[![2025-02-04-22-33-39.jpg](https://i.postimg.cc/T39YH92m/2025-02-04-22-33-39.jpg)](https://postimg.cc/JssLsjk4)

Why Does It Scan 0 Bytes?

    Precomputed Storage
        A materialized table is a physically stored table with precomputed results.
        Since the row count is already stored in metadata, BigQuery does not need to scan the actual data.

    Metadata Query Optimization
        BigQuery stores metadata about the number of rows in a materialized table.
        When you run COUNT(*), it retrieves the count directly from metadata, not by scanning the table.

    No Data Processing Required
        Normally, COUNT(*) on a regular table requires scanning at least one column.
        In materialized tables, the row count is precomputed and stored, so BigQuery skips scanning altogether.