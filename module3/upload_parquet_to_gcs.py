import fsspec


# Load the Google Service Account credentials
CREDENTIALS = "./service-account.json"
gcs_fs = fsspec.filesystem("gcs", token=CREDENTIALS)

# Define GCS path
BUCKET = "merilyn_ny_taxi"
FILENAME_TEMPLATE = "yellow_tripdata_2024-0{month}.parquet"
GCS_PATH_TEMPLATE = "gs://{bucket}/{filename}"

# Source of NY Taxi Parquet file
URL_TEMPLATE = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/{filename}"
)

# Write the NY Parquet file directly to GCS
for month in range(1, 7):
    filename = FILENAME_TEMPLATE.format(month=month)
    gcs_path = GCS_PATH_TEMPLATE.format(bucket=BUCKET, filename=filename)
    url = URL_TEMPLATE.format(filename=filename)
    with fsspec.open(url, "rb") as source, gcs_fs.open(gcs_path, "wb") as dest:
        dest.write(source.read())
    print(f"File {filename} uploaded successfully to {gcs_path}!")
