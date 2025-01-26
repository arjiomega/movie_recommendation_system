{{ 
    config(
        materialized='incremental',
        unique_key=['movie_id', 'genre_id']
    ) 
}}
WITH movies_in_increment as (
    SELECT mov.movie_id
    FROM {{ ref('dim_movie_info') }} mov
    {% if is_incremental() %}
        WHERE 
            mov.release_date >= '{{ var("start_date") }}' AND -- 2020-01-01
            mov.release_date < '{{ var("end_date") }}' -- 2020-02-01
    {% endif %}
)
SELECT
    mov.id AS movie_id,
    genre_element ->> 'id' AS genre_id
FROM {{ source('staging', 'raw_movies')  }} mov,
     LATERAL JSONB_ARRAY_ELEMENTS(mov.genres) AS genre_element
WHERE mov.id IN (SELECT movie_id FROM movies_in_increment)
