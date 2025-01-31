from typing import Literal
from airflow.operators.python import PythonOperator

from dag_utils.utils import PostgresQueryExecutor
from dag_utils.tables import (
    Table,
    StagingRawGenresTable,
    StagingRawMoviesTable,
    StagingRawCreditsTable,
    StagingRawReviewsTable
)

TABLE_NAME_TYPE = Literal[
    "staging_raw_genres_table",
    "staging_raw_movies_table",
    "staging_raw_credits_table",
    "staging_raw_reviews_table"
]

def create_schemas(postgres_executor: PostgresQueryExecutor):
    query = """CREATE SCHEMA IF NOT EXISTS staging_tmdb_data;
    CREATE SCHEMA IF NOT EXISTS dw_movies;
    CREATE SCHEMA IF NOT EXISTS app;"""
    def wrapper():
        postgres_executor.execute_query(query)
    return PythonOperator(
        task_id=f"create_schemas",
        python_callable=wrapper,
    )

class SetupDB:
    
    def __init__(self, postgres_executor: PostgresQueryExecutor):
        self.postgres_executor = postgres_executor

        self.tables: dict[str, Table] = {
            "staging_raw_genres_table": StagingRawGenresTable(),
            "staging_raw_movies_table": StagingRawMoviesTable(),
            "staging_raw_credits_table": StagingRawCreditsTable(),
            "staging_raw_reviews_table": StagingRawReviewsTable()
        }

    def create_table(
            self, 
            table_name: TABLE_NAME_TYPE
        ):
        if table_name not in self.tables:
                raise ValueError(f"table_name {table_name} is invalid. Available table names are [{', '.join(self.tables)}]")
        def wrapper():
            create_table_query = self.tables[table_name].get_create_query()
            self.postgres_executor.execute_query(create_table_query)
        return wrapper

    def __call__(self, table_name):
        return PythonOperator(
            task_id=f"create_{table_name}",
            python_callable=self.create_table(table_name),
        )