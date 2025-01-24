import os
from datetime import datetime, timedelta

from airflow import DAG

from dag_utils.utils import PostgresQueryExecutor
from ingest_tasks import (
    IngestMovieCredits, 
    IngestMovieDetails, 
    IngestMovieReviews, 
    IngestGenres,
    TMDBApiClient, 
    GetMovieIds
)
from setup_db_tasks import SetupDB, create_schemas

default_args = {
    "owner": "Richard Omega",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="tmdb_dag_2.1",
    default_args=default_args,
    start_date=datetime(2024, 10, 1),
    schedule_interval="@monthly",
    max_active_runs=5,
    catchup=True,
) as dag:

    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
    tmdb_api_client = TMDBApiClient(TMDB_API_KEY)
    postgres_executor = PostgresQueryExecutor(postgres_conn_id="postgres_default")

    # SETUP DB
    create_schema = create_schemas(postgres_executor)
    setup_db = SetupDB(postgres_executor)

    # GET MOVIE IDs
    get_movie_ids = GetMovieIds(
        task_id="get_movie_ids",
        tmdb_api_client=tmdb_api_client
    )

    # INGEST TASKS
    ingest_movies = IngestMovieDetails(
        task_id="ingest_movie_details", 
        postgres_executor=postgres_executor,
        tmdb_api_client=tmdb_api_client
    )
    ingest_reviews = IngestMovieReviews(
        task_id="ingest_tmdb_reviews", 
        postgres_executor=postgres_executor,
        tmdb_api_client=tmdb_api_client
    )
    ingest_credits = IngestMovieCredits(
        task_id="ingest_tmdb_credits", 
        postgres_executor=postgres_executor,
        tmdb_api_client=tmdb_api_client
    )
    ignest_genres = IngestGenres(
        task_id="ingest_tmdb_genres", 
        postgres_executor=postgres_executor,
        tmdb_api_client=tmdb_api_client
    )

    ## SETUP DB > GET MOVIE IDs > INGEST
    create_schema >> setup_db(table_name="staging_raw_movies_table") >> [
        setup_db(table_name="staging_raw_genres_table"),
        setup_db(table_name="staging_raw_reviews_table"),
        setup_db(table_name="staging_raw_credits_table")
    ] >> get_movie_ids() >> ingest_movies() >> [
            ingest_reviews(), ingest_credits(), ignest_genres()]
        
