

```bash
docker-compose build
docker-compose up -d
```

apis used 
https://developer.themoviedb.org/reference/discover-movie

reference
https://github.com/bardadon/imdb_data_engineering


```json
{
  "page": 1,
  "results": [
    {
      "adult": false,
      "backdrop_path": "/zOpe0eHsq0A2NvNyBbtT6sj53qV.jpg",
      "genre_ids": [
        28,
        878,
        35,
        10751
      ],
      "id": 939243,
      "original_language": "en",
      "original_title": "Sonic the Hedgehog 3",
      "overview": "Sonic, Knuckles, and Tails reunite against a powerful new adversary, Shadow, a mysterious villain with powers unlike anything they have faced before. With their abilities outmatched in every way, Team Sonic must seek out an unlikely alliance in hopes of stopping Shadow and protecting the planet.",
      "popularity": 3961.143,
      "poster_path": "/d8Ryb8AunYAuycVKDp5HpdWPKgC.jpg",
      "release_date": "2024-12-19",
      "title": "Sonic the Hedgehog 3",
      "video": false,
      "vote_average": 7.6,
      "vote_count": 505
    },
    {
      "adult": false,
      "backdrop_path": "/oHPoF0Gzu8xwK4CtdXDaWdcuZxZ.jpg",
      "genre_ids": [
        12,
        10751,
        16
      ],
      "id": 762509,
      "original_language": "en",
      "original_title": "Mufasa: The Lion King",
      "overview": "Mufasa, a cub lost and alone, meets a sympathetic lion named Taka, the heir to a royal bloodline. The chance meeting sets in motion an expansive journey of a group of misfits searching for their destiny.",
      "popularity": 3477.473,
      "poster_path": "/jbOSUAWMGzGL1L4EaUF8K6zYFo7.jpg",
      "release_date": "2024-12-18",
      "title": "Mufasa: The Lion King",
      "video": false,
      "vote_average": 7.4,
      "vote_count": 611
    },
```


1. Movies Table:

    movie_id (Primary Key)
    title
    release_date
    runtime
    language
    overview
    poster_url
    average_rating
    release_country

2. Genres Table:

    genre_id (Primary Key)
    name

3. Actors Table:

    actor_id (Primary Key)
    name
    dob (Date of Birth)
    biography
    profile_picture_url

4. Directors Table:

    director_id (Primary Key)
    name
    dob (Date of Birth)
    biography
    profile_picture_url

5. Reviews Table:

    review_id (Primary Key)
    movie_id (Foreign Key referencing Movies)
    user_id (Foreign Key referencing Users)
    review_text
    rating (User rating, typically from 1 to 10)
    created_at

6. Ratings Table:

    rating_id (Primary Key)
    movie_id (Foreign Key referencing Movies)
    user_id (Foreign Key referencing Users)
    rating_value (Value from 1 to 10)
    created_at

7. Companies Table:

    company_id (Primary Key)
    name
    logo_url
    origin_country

8. Movie_Actors (Join Table for Movies and Actors):

    movie_id (Foreign Key referencing Movies)
    actor_id (Foreign Key referencing Actors)
    role (Role played by the actor in the movie)

9. Movie_Genres (Join Table for Movies and Genres):

    movie_id (Foreign Key referencing Movies)
    genre_id (Foreign Key referencing Genres)

10. Movie_Collections (Join Table for Movies and Collections):

    movie_id (Foreign Key referencing Movies)
    collection_id (Foreign Key referencing Collections)

11. Keywords Table:

    keyword_id (Primary Key)
    keyword (Keyword or tag)

12. Movie_Keywords (Join Table for Movies and Keywords):

    movie_id (Foreign Key referencing Movies)
    keyword_id (Foreign Key referencing Keywords)

13. Collections Table:

    collection_id (Primary Key)
    name
    overview
    poster_url

14. Users Table (for reviews and ratings):

    user_id (Primary Key)
    username
    email
    password_hash
    join_date


Example Use Cases

    Finding Movies by Genre:
        You can query the Movie_Genres join table to find all movies in a particular genre.

    Getting Cast for a Movie:
        Use the Movie_Actors join table to fetch actors associated with a movie and their roles.

    Fetching Reviews for a Movie:
        Query the Reviews table to fetch all reviews related to a specific movie.

    Get Movies with High Ratings:
        Query the Ratings table to find the movies with the highest ratings.

    Movies in a Collection:
        Use the Movie_Collections join table to find all movies in a particular collection (e.g., "The Lord of the Rings").

Next Steps

    Populate Data: Use the TMDb API to fetch movie data and populate the database.
    Indexes: Create indexes on foreign keys and commonly queried columns like movie_id, genre_id, and actor_id to optimize performance.
    Normalization: Ensure the database is normalized (up to 3NF) to reduce data redundancy.