from datetime import datetime, timedelta
from airflow import DAG

default_args = {
    "owner": "Richard Omega",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}
from ingest_tmdb_data import IngestMovies, IngestReviews
from database_setup import database_setup

with DAG(
    dag_id="tmdb_dag_12",
    default_args=default_args,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2020, 5, 1),
    schedule_interval="@monthly",
    max_active_runs=1,
    catchup=True,
) as dag:

    ingest_movies = IngestMovies()
    ingest_reviews = IngestReviews()

    database_setup() >> ingest_movies.ingest_operator() >> ingest_reviews.ingest_operator()
