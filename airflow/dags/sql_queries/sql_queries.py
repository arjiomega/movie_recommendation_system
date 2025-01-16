create_schema = """
CREATE SCHEMA IF NOT EXISTS raw_tmbd_data;
CREATE SCHEMA IF NOT EXISTS staging_tmbd_data;
CREATE SCHEMA IF NOT EXISTS analytics_tmbd_data;
"""

class CreateTables:
    create_raw_movies_table = """
    CREATE TABLE IF NOT EXISTS raw_tmbd_data.raw_movies (
        id BIGINT PRIMARY KEY,                    -- Identifier as primary key
        title TEXT NOT NULL,                      -- Title of the movie
        original_title TEXT NOT NULL,             -- Original title of the movie
        release_date DATE NOT NULL,               -- Release date of the movie
        popularity NUMERIC(10, 3) NOT NULL,       -- Popularity score
        vote_average REAL NOT NULL,               -- Average vote score
        vote_count INTEGER NOT NULL,              -- Number of votes
        adult BOOLEAN NOT NULL,                   -- Is the movie adult content
        video BOOLEAN NOT NULL,                   -- Is the movie a video
        overview TEXT,                            -- Description of the movie
        genre_ids INTEGER[] NOT NULL,             -- List of genre IDs
        original_language VARCHAR(2) NOT NULL,    -- Original language of the movie
        backdrop_path TEXT,                       -- Path to the backdrop image
        poster_path TEXT                          -- Path to the poster image
    );
    """
    create_raw_reviews_table = """
    CREATE TABLE IF NOT EXISTS raw_tmbd_data.raw_reviews (
        id TEXT PRIMARY KEY,          
        movie_id BIGINT,            
        author TEXT,
        content TEXT,
        created_at TIMESTAMPTZ,       
        updated_at TIMESTAMPTZ,
        url TEXT,
        author_details JSONB,         
        CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES raw_tmbd_data.raw_movies(id)
    );
    """


if __name__ == "__main__":
    print(CreateTables.create_raw_movies_table)