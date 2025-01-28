{{ 
    config(
        materialized='incremental',
        unique_key='language_id'
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
SELECT DISTINCT
    language_element ->> 'iso_639_1' AS language_id,
    language_element ->> 'name' AS language_name,
    language_element ->> 'english_name' AS english_name
FROM {{ source('staging', 'raw_movies')  }} mov,
     LATERAL JSONB_ARRAY_ELEMENTS(mov.spoken_languages) AS language_element
WHERE mov.id IN (SELECT movie_id FROM movies_in_increment)
