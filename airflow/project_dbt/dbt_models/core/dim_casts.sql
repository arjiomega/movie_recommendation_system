{{ 
    config(
        materialized='incremental',
        unique_key='cast_id'
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
    cast_element ->> 'id' AS cast_id,
    cast_element ->> 'name' AS "name",
    cast_element ->> 'adult' AS adult,
    cast_element ->> 'order' AS order,
    cast_element ->> 'gender' AS gender,
    cast_element ->> 'character' AS "character",
    cast_element ->> 'credit_id' AS credit_id,
    cast_element ->> 'popularity' AS popularity,
    cast_element ->> 'profile_path' AS profile_path,
    cast_element ->> 'original_name' AS original_name,
    cast_element ->> 'known_for_department' AS known_for_department
FROM {{ source('staging', 'raw_credits')  }} creds,
    LATERAL JSONB_ARRAY_ELEMENTS(creds.cast) AS cast_element
WHERE creds.id IN (SELECT movie_id FROM movies_in_increment)
