{{ 
    config(
        materialized='incremental',
        unique_key=['movie_id', 'collection_id']
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
    mov.belongs_to_collection ->> 'id' AS collection_id
FROM {{ source('staging', 'raw_movies')  }} mov
WHERE mov.id IN (SELECT movie_id FROM movies_in_increment)
