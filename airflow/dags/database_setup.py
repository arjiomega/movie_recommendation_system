from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from sql_queries import sql_queries

def create_schemas(conn_id="postgres_default"):
    """
    Raw Schema	
    - Stores the data in its raw, unprocessed format as it was ingested from the source system.	
    - Unstructured or semi-structured data (e.g., JSON).	
    - Raw TMDB API response in JSON format
    Staging Schema	
    - Stores the data after it has been ingested and minimally transformed (e.g., parsing, validation).	
    - Structured but not fully cleaned or transformed data.	
    - Flattened TMDB data into tables
    Analytics Schema	
    - Stores the cleaned, transformed, and aggregated data optimized for analysis and reporting.	
    - Fully cleaned, aggregated, and optimized for queries.	
    - Aggregated TMDB data for analysis
    """

    return SQLExecuteQueryOperator(
        task_id="create_schemas",
        conn_id=conn_id,
        sql=sql_queries.create_schema
    )

class CreateTables:
    def __init__(self, conn_id="postgres_default"):
        self.conn_id = conn_id

    def create_raw_movies_table(self):
        return SQLExecuteQueryOperator(
            task_id="create_raw_movies_table",
            conn_id=self.conn_id,
            sql=sql_queries.CreateTables.create_raw_movies_table
        )

    def create_raw_reviews_table(self):
        return SQLExecuteQueryOperator(
            task_id="create_raw_reviews_table",
            conn_id=self.conn_id,
            sql=sql_queries.CreateTables.create_raw_reviews_table
        )

def database_setup():
    create_tables = CreateTables()
    return [
        create_schemas(),
        create_tables.create_raw_movies_table(),
        create_tables.create_raw_reviews_table()
    ]