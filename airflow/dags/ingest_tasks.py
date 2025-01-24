import calendar
from abc import ABC, abstractmethod
from typing import Callable, Literal
from urllib.parse import urlencode, urljoin

from airflow.operators.python import PythonOperator

from dag_utils.utils import PostgresQueryExecutor, TMDBApiClient
from dag_utils.tables import (
    Table, 
    StagingRawCreditsTable, 
    StagingRawGenresTable, 
    StagingRawMoviesTable, 
    StagingRawReviewsTable
)

class Ingest(ABC):
    def __init__(
            self,
            table: Table,
            postgres_executor: PostgresQueryExecutor,
            tmdb_api_client: TMDBApiClient
        ):
        self.table = table
        self.postgres_executor = postgres_executor
        self.tmdb_api_client = tmdb_api_client

    @abstractmethod
    def ingest(self, url):
        data = self.tmdb_api_client.fetch(url)
        insert_query = self.table.get_insert_query(data)
        self.postgres_executor.execute_query(insert_query)

    def __call__(self, task_id: str, python_callable: Callable) -> PythonOperator:
        return PythonOperator(
            task_id=task_id,
            python_callable=python_callable,
        )
        
class GetMovieIds:
    def __init__(self, task_id, tmdb_api_client: TMDBApiClient):
        self.task_id = task_id
        self.tmdb_api_client = tmdb_api_client
        self.base_url = "https://api.themoviedb.org/3/discover/movie"

    def _get_start_end_dates(self, logical_date):
        year, month = logical_date.strftime("%Y"), logical_date.strftime("%m")
        last_day = calendar.monthrange(int(year), int(month))[1]

        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{last_day}"

        return start_date, end_date

    def get_movie_ids(self, logical_date, ti):
        
        start_date, end_date = self._get_start_end_dates(logical_date)

        params = {
            "language": "en-US",
            "page": 1,
            "primary_release_date.gte": start_date,
            "primary_release_date.lte": end_date,
            "sort_by": "popularity.desc",
        }
        generate_url = lambda params: urljoin(self.base_url, f"?{urlencode(params)}")

        movie_ids = []
        max_page = 500 # temporary

        while params["page"] <= max_page:
            full_url = generate_url(params)
            data = self.tmdb_api_client.fetch(full_url)
            movie_ids.extend([result["id"] for result in data["results"]])

            max_page = data["total_pages"] if data["total_pages"] <= 500 else 500
            print(f"Successfully loaded page {params["page"]} / {max_page}")

            params["page"] += 1

        print(f"Number of movie ids obtained {len(movie_ids)}")            
        ti.xcom_push(key="movie_ids", value=movie_ids)

    def __call__(self):
        return PythonOperator(
            task_id=self.task_id,
            python_callable=self.get_movie_ids,
        )

class IngestMovies(Ingest):
    def __init__(
            self,
            task_id: str,
            fetch_task: Literal["details", "reviews", "credits"],
            table: Table,
            postgres_executor: PostgresQueryExecutor,
            tmdb_api_client: TMDBApiClient
        ):
        self.task_id = task_id
        self.table = table
        self.postgres_executor = postgres_executor
        self.tmdb_api_client = tmdb_api_client
        self.fetch_task = fetch_task

    def ingest(self, movie_ids: list[int], transform_fn: Callable = None):
        data_list = self.tmdb_api_client.fetch_multiple_movie_data(movie_ids, self.fetch_task)
        if transform_fn:
            data_list = transform_fn(data_list)
        insert_query = self.table.get_insert_query(data_list)
        self.postgres_executor.execute_query(insert_query)

    def __call__(self, python_callable):
        return super().__call__(self.task_id, python_callable)


class IngestGenres(Ingest):
    def __init__(self, task_id: str, postgres_executor: PostgresQueryExecutor, tmdb_api_client: TMDBApiClient):
        self.task_id = task_id
        table = StagingRawGenresTable()
        super().__init__(table, postgres_executor, tmdb_api_client)

    def ingest(self):
        url = "https://api.themoviedb.org/3/genre/movie/list"
        super().ingest(url)

    def __call__(self):
        return super().__call__(self.task_id, self.ingest)

class IngestMovieDetails(IngestMovies):
    def __init__(self, task_id: str, postgres_executor: PostgresQueryExecutor, tmdb_api_client: TMDBApiClient):
        table = StagingRawMoviesTable()
        super().__init__(
            fetch_task="details", 
            task_id=task_id,
            table=table, 
            postgres_executor=postgres_executor, 
            tmdb_api_client=tmdb_api_client
        )

    def ingest(self, ti):
        movie_ids = ti.xcom_pull(task_ids='get_movie_ids', key='movie_ids')
        # movie_ids = [1411556]
        super().ingest(movie_ids)

    def __call__(self):
        return super().__call__(self.ingest)

class IngestMovieReviews(IngestMovies):
    def __init__(self, task_id: str, postgres_executor: PostgresQueryExecutor, tmdb_api_client: TMDBApiClient):
        table = StagingRawReviewsTable()
        super().__init__(
            fetch_task="reviews", 
            task_id=task_id,
            table=table, 
            postgres_executor=postgres_executor, 
            tmdb_api_client=tmdb_api_client
        )

    def ingest(self, ti):
        movie_ids = ti.xcom_pull(task_ids='get_movie_ids', key='movie_ids')
        super().ingest(movie_ids)

    def __call__(self):
        return super().__call__(self.ingest)

class IngestMovieCredits(IngestMovies):
    def __init__(self, task_id: str, postgres_executor: PostgresQueryExecutor, tmdb_api_client: TMDBApiClient):
        table = StagingRawCreditsTable()
        super().__init__(
            fetch_task="credits", 
            task_id=task_id,
            table=table, 
            postgres_executor=postgres_executor, 
            tmdb_api_client=tmdb_api_client
        )

    def ingest(self, ti):
        movie_ids = ti.xcom_pull(task_ids='get_movie_ids', key='movie_ids')
        # movie_ids = [1411556]
        super().ingest(movie_ids)

    def __call__(self):
        return super().__call__(self.ingest)