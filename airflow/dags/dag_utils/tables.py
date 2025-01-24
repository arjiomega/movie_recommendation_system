
from abc import ABC, abstractmethod
from .utils import StringFormatter

class Table(ABC):
 
    def __init__(self, schema, table_name, columns):
        self.schema = schema
        self.table_name = table_name
        self.columns = columns
        self.stringformatter = StringFormatter()

    @abstractmethod
    def get_create_query(self, additional_query: str = ''):
        query = f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.table_name} (\n"
        column_definitions = [f'    "{column_name}" {type}' for column_name, type in self.columns.items()]
        query += ",\n".join(column_definitions)
        query += additional_query
        query += "\n);"
        return query

    @abstractmethod
    def get_insert_query(self, values: list[dict]):
        ordered_values_list = [self.update_values_order(value) for value in values]

        query = f"INSERT INTO {self.schema}.{self.table_name} (\n"
        column_definitions = [f'    "{column_name}"' for column_name in self.columns]
        query += ",\n".join(column_definitions)
        query += "\n) VALUES \n"

        query += ",\n".join(ordered_values_list)
        query += "\nON CONFLICT(id) DO NOTHING;"

        return query

    def update_values_order(self, row):
      
        ordered_row = [
            f"CAST({self.stringformatter.transform(row[column_name], column_type)}"+f" AS {column_type.split(" ")[0]})"
            for column_name, column_type in self.columns.items()
        ]

        ordered_row = ', \n'.join(ordered_row)
        ordered_row = "(\n" + ordered_row + "\n)"

        return ordered_row




class StagingRawMoviesTable(Table):
    def __init__(self, schema="staging_tmdb_data", table_name="raw_movies"):
        self.columns = {
            "id": "BIGINT PRIMARY KEY",
            "adult":  "BOOLEAN",
            "backdrop_path":  "TEXT",
            "budget":  "BIGINT",
            "homepage":  "TEXT",
            "imdb_id":  "TEXT",
            "original_language":  "TEXT",
            "original_title":  "TEXT",
            "overview":  "TEXT",
            "popularity":  "NUMERIC",
            "poster_path":  "TEXT",
            "release_date":  "DATE",
            "revenue":  "BIGINT",
            "runtime":  "INT",
            "status":  "TEXT",
            "tagline":  "TEXT",
            "title":  "TEXT",
            "video":  "BOOLEAN",
            "vote_average":  "NUMERIC",
            "vote_count":  "INT",
            "genres":  "JSONB",
            "production_companies":  "JSONB",
            "production_countries":  "JSONB",
            "spoken_languages":  "JSONB",
            "belongs_to_collection":  "JSONB"
        }        
        super().__init__(schema, table_name, self.columns)

    def get_create_query(self):
        return super().get_create_query()
    
    def get_insert_query(self, values: list[dict]):
        return super().get_insert_query(values)


class StagingRawReviewsTable(Table):
    def __init__(self, schema='staging_tmdb_data', table_name='raw_reviews'):
        self.columns = {
            "id": "TEXT PRIMARY KEY",          
            "movie_id": "BIGINT",            
            "author": "TEXT",
            "content": "TEXT",
            "created_at": "TIMESTAMPTZ",       
            "updated_at": "TIMESTAMPTZ",
            "url": "TEXT",
            "author_details": "JSONB",    
        }
        super().__init__(schema, table_name, self.columns)

    def get_create_query(self):
        additional_query = ',\n CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES staging_tmdb_data.raw_movies(id)'
        return super().get_create_query(additional_query)
    
    def get_insert_query(self, values: list[dict]):
        return super().get_insert_query(values)

class StagingRawGenresTable(Table):
    def __init__(self, schema='staging_tmdb_data', table_name='raw_genres'):
        self.columns = {
            "id": "BIGINT PRIMARY KEY",
            "name": "TEXT NOT NULL"
        }
        super().__init__(schema, table_name, self.columns)

    def get_create_query(self):
        return super().get_create_query()

    def get_insert_query(self, values: dict):
        return super().get_insert_query(values["genres"])

class StagingRawCreditsTable(Table):
    def __init__(self, schema='staging_tmdb_data', table_name='raw_credits'):
        self.columns = {
            "id": "BIGINT PRIMARY KEY",
            "cast": "JSONB",
            "crew": "JSONB"
        }
        super().__init__(schema, table_name, self.columns)

    def get_create_query(self):
        return super().get_create_query()

    def get_insert_query(self, values: list[dict]):
        return super().get_insert_query(values)

if __name__ == "__main__":
    staging_raw_movies = StagingRawMoviesTable()

    import requests


    url = "https://api.themoviedb.org/3/movie/12201?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkM2IwNWEzOWUzYWZhZWEzNmM0YWRlNmUwNzRiMzdkYiIsIm5iZiI6MTY3Njc2ODIxOC4xNDcsInN1YiI6IjYzZjE3M2RhMTUzNzZjMDA4MzM2MGQzYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.hY-OlHkv8a-cjw_gcggdaH7bYbMc5W05-xaVJNwA4TE"
    }

    response = requests.get(url, headers=headers)

    sample_values = response.json()
    query = staging_raw_movies.get_insert_query([sample_values, sample_values])
    print(query)

    import psycopg2

    # Connect to your PostgreSQL database
    connection = psycopg2.connect(
        dbname="movie_db",
        user="airflow",
        password="airflow",
        host="localhost",  # e.g., "localhost" or an IP address
        port="5432"   # e.g., "5432"
    )

    cursor = connection.cursor()

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()