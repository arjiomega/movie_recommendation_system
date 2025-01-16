
import time
import os
import requests
from urllib.parse import urlencode, urljoin
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import calendar

class IngestMovies:
    def __init__(self, postgres_conn_id="postgres_default"):
        self.TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
        self.postgres_conn_id = postgres_conn_id
        self.base_url = "https://api.themoviedb.org/3/discover/movie"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_API_KEY}"
        }

    def _get_start_end_dates(self, logical_date):
        year, month = logical_date.strftime("%Y"), logical_date.strftime("%m")
        last_day = calendar.monthrange(int(year), int(month))[1]

        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{last_day}"

        return start_date, end_date

    def _get_query_params(self, logical_date, page):
        start_date, end_date = self._get_start_end_dates(logical_date)

        return {
            "language": "en-US",
            "page": page,
            "primary_release_date.gte": start_date,
            "primary_release_date.lte": end_date,
            "sort_by": "popularity.desc",
        }

    def build_full_url(self, page, logical_date):
        query_params = self._get_query_params(logical_date, page)
        return urljoin(self.base_url, f"?{urlencode(query_params)}")

    def fetch_tmdb_movies(self, logical_date):

        movies_list = []

        current_page = 1
        max_page = 500 # temporary

        while current_page < max_page+1:
            full_url = self.build_full_url(current_page, logical_date)

            response = requests.get(full_url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            movies_list += data["results"]
            max_page = data["total_pages"] if data["total_pages"] <= 500 else 500

            # pause if page is divisible by 50 (api rate limitation is 50 requests/sec)
            if current_page % 50 == 0:
                time.sleep(2)

            current_page += 1

        return movies_list

    def insert_movie_records(self, movies_list):
        base_sql = """
        INSERT INTO raw_tmbd_data.raw_movies (
            id, title, original_title, release_date, popularity, vote_average, vote_count,
            adult, video, overview, genre_ids, original_language, backdrop_path, poster_path
        ) VALUES
        """

        values_list = []

        # Loop through the movie data and format each row
        for row in movies_list:
            # Escape single quotes and format the row values
            formatted_row = (
                f"('{str(row['id'])}', "
                f"'{str(row['title']).replace('\'', '\'\'')}', "
                f"'{str(row['original_title']).replace('\'', '\'\'')}', "
                f"'{str(row['release_date'])}', "
                f"{row['popularity']}, "
                f"{row['vote_average']}, "
                f"{row['vote_count']}, "
                f"'{str(row['adult']).replace('\'', '\'\'')}', "
                f"'{str(row['video']).replace('\'', '\'\'')}', "
                f"'{str(row['overview']).replace('\'', '\'\'')}', "
                f"'{str(row['genre_ids']).replace('[', '{').replace(']', '}').replace('\'', '\'\'')}', "
                f"'{str(row['original_language']).replace('\'', '\'\'')}', "
                f"'{str(row['backdrop_path']).replace('\'', '\'\'')}', "
                f"'{str(row['poster_path']).replace('\'', '\'\'')}')"
            )
            
            # Append the formatted row to the list
            values_list.append(formatted_row)

        final_sql = base_sql + ",\n".join(values_list) + "\nON CONFLICT(id) DO NOTHING;"

        print(final_sql)

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn = hook.get_conn()

        cur = conn.cursor()

        cur.execute(final_sql)

        conn.commit()
        cur.close()
        conn.close()

    def ingest(self, logical_date):

        movies_list = self.fetch_tmdb_movies(logical_date)
        self.insert_movie_records(movies_list)

    def ingest_operator(self):
        return PythonOperator(
            task_id="ingest_tmdb_movies",
            python_callable=self.ingest,
        ) 
    
        

class IngestReviews:
    def __init__(self, postgres_conn_id="postgres_default"):
        self.TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
        self.postgres_conn_id = postgres_conn_id
        self.base_url_gen = lambda movie_id: f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.TMDB_API_KEY}"
        }

        self.request_counter = 0

    def _get_start_end_dates(self, logical_date):
        year, month = logical_date.strftime("%Y"), logical_date.strftime("%m")
        last_day = calendar.monthrange(int(year), int(month))[1]

        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{last_day}"

        return start_date, end_date

    def build_full_url(self, page, movie_id):
        query_params = {"language": "en-US", "page": page}
        return urljoin(self.base_url_gen(movie_id), f"?{urlencode(query_params)}")

    def _get_movie_ids_from_date(self, logical_date):
        start_date, end_date = self._get_start_end_dates(logical_date)

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn = hook.get_conn()
        cur = conn.cursor()

        cur.execute(
            f"""
                SELECT id FROM raw_tmbd_data.raw_movies
                WHERE release_date >= '{start_date}' AND release_date < '{end_date}'
                ORDER BY release_date
            """
        )
        results = cur.fetchall()

        cur.close()
        conn.close()

        return [result[0] for result in results]

    def fetch_tmdb_reviews(self, movie_id):

        reviews_list = []

        current_page = 1
        max_page = 500 # temporary

        while current_page < max_page+1:
            full_url = self.build_full_url(current_page, movie_id)

            response = requests.get(full_url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            reviews_list += data["results"]
            max_page = data["total_pages"] if data["total_pages"] <= 500 else 500

            self.request_counter += 1
            current_page += 1

            # pause if page is divisible by 50 (api rate limitation is 50 requests/sec)
            if (current_page % 50 == 0) | (self.request_counter % 50 == 0):
                time.sleep(2)

        return reviews_list

    def insert_review_records(self, reviews_list, movie_id):
        import json
        base_sql = """
        INSERT INTO raw_tmbd_data.raw_reviews (
            id, movie_id, author, content, created_at, updated_at, url, author_details
        ) VALUES
        """

        """
        [
        {
            'author': 'CinemaSerf', 
            'author_details': 
                {
                    'name': 'CinemaSerf', 
                    'username': 'Geronimo1967', 
                    'avatar_path': '/yz2HPme8NPLne0mM8tBnZ5ZWJzf.jpg', 
                    'rating': 6.0
                }, 
            'content': "I sometime quite like these rather thinly disguised and experimental 
                        looking theatrical movies, and though this is hugely over-scripted, it's 
                        still quite an interesting prognostication on just how an illicit relationship 
                        between Sidney Lumet and Montgomery Clift might have played out. The former 
                        (Aaron Fors) is also the narrator as he befriends the latter (Gavin Adams) after 
                        a drunken conversation in an alleyway. What now ensues is heavily stylised and 
                        entirely speculative but there is a spark of chemistry between the two men and 
                        it does illustrate well the ridiculous lengths men had to go to to cover up their 
                        sexuality when it didn't conform to the designs of the studios, the PR men, the 
                        press or even the law. Now this is by no means a great production, indeed I think 
                        it might have looked better had it stayed within the confines of a stage setting 
                        rather than move out into the big bright world, but as a piece of challenging cinema 
                        it's not bad at all. No, I probably wouldn't watch it again and the dramatic elements 
                        are basic and sometimes downright hammy, but it's still just about worth a watch as 
                        an amateur-looking piece of what might pass for Hollywood Babylon!", 
            'created_at': '2024-01-17T10:54:03.829Z', 
            'id': '65a7b1cbaa78980128627796',  # DONE
            'updated_at': '2024-01-17T10:54:04.087Z', 
            'url': 'https://www.themoviedb.org/review/65a7b1cbaa78980128627796'
        }
        ]
        """

        values_list = []

        # Loop through the movie data and format each row
        for row in reviews_list:
            # Escape single quotes and format the row values
            

            formatted_row = (
                f"('{str(row['id']).replace('\'', '\'\'')}', "
                f"'{str(movie_id).replace('\'', '\'\'')}', "
                f"'{str(row['author']).replace('\'', '\'\'')}', "
                f"'{str(row['content']).replace('\'', '\'\'')}', "
                f"'{str(row['created_at']).replace('\'', '\'\'')}', "
                f"'{str(row['updated_at']).replace('\'', '\'\'')}', "
                f"'{str(row['url']).replace('\'', '\'\'')}', "
                f"'{json.dumps(row['author_details']).replace('\'', '\'\'')}')"
            )
            
            # Append the formatted row to the list
            values_list.append(formatted_row)

        final_sql = base_sql + ",\n".join(values_list) + "\nON CONFLICT(id) DO NOTHING;"

        print(final_sql)

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn = hook.get_conn()

        cur = conn.cursor()

        cur.execute(final_sql)

        conn.commit()
        cur.close()
        conn.close()

        

    def ingest(self, logical_date):

        movie_ids_list = self._get_movie_ids_from_date(logical_date)

        for movie_id in movie_ids_list:
            reviews_list = self.fetch_tmdb_reviews(movie_id)
            if reviews_list:
                # print(reviews_list)
                self.insert_review_records(reviews_list, movie_id)

            # print(f"movie_id {movie_id} has {len(reviews_list)} rows.")

    def ingest_operator(self):
        return PythonOperator(
            task_id="ingest_tmdb_reviews",
            python_callable=self.ingest,
        ) 






    


