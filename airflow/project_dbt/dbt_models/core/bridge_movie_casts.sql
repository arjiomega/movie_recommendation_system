{{ 
    config(
        materialized='incremental',
        unique_key=['movie_id', 'cast_id']
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
    creds.id AS movie_id,
    cast_element ->> 'id' AS cast_id
FROM {{ source('staging', 'raw_credits')  }} creds,
    LATERAL JSONB_ARRAY_ELEMENTS(creds.cast) AS cast_element
WHERE creds.id IN (SELECT movie_id FROM movies_in_increment)
