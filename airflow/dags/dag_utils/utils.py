import json
import time
from typing import Literal

import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook

class StringFormatter:
    def __init__(self):
        pass
    def _fix_empty_string(self, value):
        return value if value not in [None, '', 'None'] else 'NULL' 
    def transform(self, value, column_type):
        value = self._fix_empty_string(value)

        if column_type in ['BIGINT', 'BIGINT PRIMARY KEY', 'NUMERIC', 'INT', 'TIMESTAMPTZ']:
            return f"'{str(value)}'" if value != 'NULL' else value
        elif 'DATE' in column_type:
            return f"'{str(value)}'" if value != 'NULL' else value
        elif 'TEXT' in column_type:
            transformed_value = value.replace("'", "''")
            return f"'{transformed_value}'"
        elif 'BOOLEAN' in column_type:
            return  str(value).upper()
        elif 'JSONB' in column_type:
            return f"'{json.dumps(value).replace("'", "''")}'" if value != 'NULL' else value
        else:
            raise ValueError(f"'{column_type}' is an invalid column_type.")
        
class PostgresQueryExecutor:
    def __init__(self, postgres_conn_id="postgres_default"):
        self.postgres_conn_id = postgres_conn_id

    def execute_query(self, query):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn = hook.get_conn()

        try:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Error executing query: {query}. Error: {e}") from e
        finally:
            cur.close()
            conn.close()


class TMDBApiClient:
    def __init__(self, TMDB_API_KEY):
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}"
        }

    def fetch(self, url, retries=5, delay=1) -> dict:
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise

    def _get_url(self, movie_id: int, fetch_task: Literal["details", "reviews", "credits"], page: int = None):
        movie_url = "https://api.themoviedb.org/3/movie/"
        if fetch_task == "details":
            return movie_url + str(movie_id)
        elif fetch_task == "reviews":
            return movie_url + str(movie_id) + f"/reviews?page={page}"
        elif fetch_task == "credits":
            return movie_url + str(movie_id) + "/credits"
        else:
            raise ValueError(f"fetch task: {fetch_task} is invalid.")

    def _loop_pages(self, movie_id, fetch_task) -> list[dict]:
    
        if fetch_task != "reviews":
            raise ValueError("fetch_task = 'reviews' is required.")

        page = 1
        max_page = 500 # temporary

        data_list = []

        while page <= max_page:
            url = self._get_url(movie_id, fetch_task, page)
            data = self.fetch(url)

            for review in data["results"]:
                updated_data = {
                    "id": review["id"],
                    "movie_id": movie_id,
                    "author": review["author"],
                    "content": review["content"],
                    "created_at": review["created_at"],
                    "updated_at": review["updated_at"],
                    "url": review["url"],
                    "author_details": review["author_details"]
                }
                data_list.append(updated_data)

            page += 1
            max_page = data["total_pages"] if data["total_pages"] <= 500 else 500

        return data_list

    def fetch_movie_data(self, movie_id, fetch_task: Literal["details", "reviews", "credits"]):
        url = self._get_url(movie_id, fetch_task)
        return self.fetch(url)
        
    def fetch_multiple_movie_data(
            self, 
            movie_ids: list[int], 
            fetch_task: Literal["details", "reviews", "credits"]
        ) -> list[dict]:
        data_list = []

        for idx, movie_id in enumerate(movie_ids):
            if fetch_task in ["details", "credits"]:
                data_list.append(self.fetch_movie_data(movie_id, fetch_task))
            elif fetch_task == "reviews":
                data_list.extend(self._loop_pages(movie_id, fetch_task))
            else:
                raise ValueError(f"fetch task {fetch_task} is invalid.")
            
            if (idx % 100 == 0) | ((idx+1) == len(movie_ids)):
                print(f"successfully fetched {idx+1} / {len(movie_ids)} for task: {fetch_task}")
        
        return data_list