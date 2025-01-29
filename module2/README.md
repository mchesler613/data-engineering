# Data Engineering Module 2 Answers for Questions 1-6

## Question 1

*Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?*

```
128.3 MB
134.5 MB
364.7 MB
692.6 MB
```

To solve this, I executed the `flows/merilyn_gcp_taxi.yaml` script in kestra selecting `2020` as year, `yellow` as `taxi type` and `12` as month.

[![2025-01-28-14-33-19.jpg](https://i.postimg.cc/J0M9P5Lj/2025-01-28-14-33-19.jpg)](https://postimg.cc/472L3tn3)

The result can be seen in GCS.

[![2025-01-28-14-36-11.jpg](https://i.postimg.cc/prW6DVfZ/2025-01-28-14-36-11.jpg)](https://postimg.cc/mznj4s6z)

giving the answer to be `128.3 MB`.

## Question 2

*What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
```
{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv
green_tripdata_2020-04.csv
green_tripdata_04_2020.csv
green_tripdata_2020.csv*
```

To solve this, I ran the `flows/merilyn_gcp_taxi.yaml` script in kestra selecting `2020` as year, `green` as `taxi type` and `4` as month.

I then check the execution logs in the Extract task, pick the Output and look at the value.

[![2025-01-28-14-51-19.jpg](https://i.postimg.cc/T32LDz5c/2025-01-28-14-51-19.jpg)](https://postimg.cc/yk58qrPJ)

[![2025-01-28-14-50-50.jpg](https://i.postimg.cc/bN9SdyrJ/2025-01-28-14-50-50.jpg)](https://postimg.cc/mthg5GQf)

So the answer is `green_tripdata_2020-04.csv`.

## Question 3

*How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?*
```
13,537.299
24,648,499
18,324,219
29,430,127
```

To solve this, I ran the `flows/merilyn_gcp_taxi_scheduled` script in kestra selecting a scheduled trigger for `yellow` taxi to run between `2020-01-01` and `2020-12-31` and adding a backfill label.

[![2025-01-28-15-02-56.jpg](https://i.postimg.cc/tT8v1drh/2025-01-28-15-02-56.jpg)](https://postimg.cc/N97kSXvM)

I then check that the csv files are uploaded correctly on GCS.

[![2025-01-28-15-04-12.jpg](https://i.postimg.cc/7hV7vwTf/2025-01-28-15-04-12.jpg)](https://postimg.cc/648TnscX)

I then ran an SQL query on the GBQ tables.

[![2025-01-28-15-07-48.jpg](https://i.postimg.cc/jd12DDKR/2025-01-28-15-07-48.jpg)](https://postimg.cc/4mzsMNm0)

The answer is `24,648,499`

## Question 4

*How many rows are there for the Green Taxi data for all CSV files in the year 2020?*
```
5,327,301
936,199
1,734,051
1,342,034
```

To solve this, I ran the `flows/merilyn_gcp_taxi_scheduled` script in kestra selecting a scheduled trigger for `green` taxi to run between `2020-01-01` and `2020-12-31` and adding a backfill label.

[![2025-01-28-15-44-59.jpg](https://i.postimg.cc/QCq3mfnr/2025-01-28-15-44-59.jpg)](https://postimg.cc/H8jRs9gS)


I then check that all the scheduled flows are executed.

[![2025-01-28-15-51-24.jpg](https://i.postimg.cc/GmW5BkqP/2025-01-28-15-51-24.jpg)](https://postimg.cc/5Xm3TFcj)

I then check the GCS storage for 2020 green taxi .csv files.

[![2025-01-28-15-52-46.jpg](https://i.postimg.cc/YqVXV6Kc/2025-01-28-15-52-46.jpg)](https://postimg.cc/bsxHS2wL)


I then ran an SQL query for all the `unique_row_id` found in these .csv filenames.

[![2025-01-28-15-54-31.jpg](https://i.postimg.cc/ZqmLtjwQ/2025-01-28-15-54-31.jpg)](https://postimg.cc/pm0jKQbQ)

So, the answer is `1,734,051`.

## Question 5

*How many rows are there for the Yellow Taxi data for the March 2021 CSV file?*
```
1,428,092
706,911
1,925,152
2,561,031
```

To solve this, I ran the `flows/merilyn_gcp_taxi.yaml` script for the `yellow` taxi, year `2021` and month `03`.

Check that the .csv file is uploaded to GCS.

[![2025-01-28-16-53-00.jpg](https://i.postimg.cc/yxpYHV0N/2025-01-28-16-53-00.jpg)](https://postimg.cc/0KmqG1Wg)

Run the SQL query to count the number of unique_row_ids in the GBQ table.

[![2025-01-28-16-55-01.jpg](https://i.postimg.cc/bvfY8VS1/2025-01-28-16-55-01.jpg)](https://postimg.cc/Hr31922L)

The answer is `1,925,152`.

## Question 6

*How would you configure the timezone to New York in a Schedule trigger?*
```
Add a timezone property set to EST in the Schedule trigger configuration
Add a timezone property set to America/New_York in the Schedule trigger configuration
Add a timezone property set to UTC-5 in the Schedule trigger configuration
Add a location property set to New_York in the Schedule trigger configuration
```

To answer this question, I searched the Kestra official documentation and found this [Link](https://kestra.io/docs/workflow-components/triggers/schedule-trigger).

[![2025-01-28-17-01-12.jpg](https://i.postimg.cc/25XDyHVH/2025-01-28-17-01-12.jpg)](https://postimg.cc/gwR5BHyR)

So, the answer would be `Add a timezone property set to America/New_York in the Schedule trigger configuration`.

## Developer Environment Setup

### Service Account Credentials

To use the GCP setup for kestra workflows, I created the service account credentials and encode it as explained in this [tutorial](https://github.com/m-t-a97/docs/blob/main/content/docs/15.how-to-guides/google-credentials.md).

I saved the encoded JSON in this file, `.env_encoded`. I then modified the kestra's `docker-compose.yml` to include this file:
```
kestra:
    env_file: .env_encoded
```

In each of the gcp yaml flows, I replaced the `GCP_CRED` with `GCP_SERVICE_ACCOUNT` variable like so:

```
serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
```
### docker-compose.yml

To dockerize the kestra, postgres and pgadmin services inside docker, do `docker compose up -d` at the folder where the docker-compose.yml lives.

- Access `pgadmin` at the browser, `http://localhost:8080`
    - Add a `postgres` server in `pgadmin` based on the docker-compose.yml configuration 
- Access `kestra` at the browser, `http://localhost:8082`

### Terraform for GCS and GBQ resource creation

I used `terraform` to automate the creation of GCS bucket and GBQ dataset. Look in the `terraform` folder for the associated files.  I ran:
```
$ terraform init
$ terraform apply -var 'project=silent-blade-447917-q2' -auto-approve
```

## Bonus Experimentation

In the kestra `postgres` yaml flows, I decided to experiment with using an extended version of the `ingest_data.py` from module 1 to implement an ETL pipeline here:
- `flows/merilyn_ingest_data.yaml` and 
- `flows/merilyn_ingest_data_scheduled.yaml`.  

See the `scripts` folder that is maintained by `poetry` and `pyenv` for more information.

The `ingest_data.py` script reads only from `.parquet` files stored in the NY Taxi website.  I found that there are discrepanices in the `green` taxi `2020` data between .csv and .parquet.

- parquet data

[![2025-01-23-21-48-42.jpg](https://i.postimg.cc/bvn7Yzfv/2025-01-23-21-48-42.jpg)](https://postimg.cc/bGzC3fJX)

- csv data

[![2025-01-25-19-10-50.jpg](https://i.postimg.cc/hjqHfHK1/2025-01-25-19-10-50.jpg)](https://postimg.cc/DWBCNpJS)

Therefore, I couldn't use this Python script ETL pipeline to solve the homework problems above based on the discrepancies. But I could use this for my final project.

