import dlt
import pp

from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


# Define the API resource for NYC taxi data
# Pass the name of the resource that will be used as the table name
@dlt.resource(name="taxi_rides")
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    # pass API endpoint for retrieving taxi ride data to paginate
    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page   # <--- yield data to manage memory


# define new dlt pipeline
pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data",
)

# run the pipeline with the new resource
load_info = pipeline.run(ny_taxi, write_disposition="replace")
print(load_info)

# explore loaded data
df = pipeline.dataset(dataset_type="default").taxi_rides.df()
pp(df)
