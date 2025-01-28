{{ 
    config(
        materialized='incremental',
        unique_key='crew_id'
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
    crew_element ->> 'id' AS crew_id,
    crew_element ->> 'job' AS job,
    crew_element ->> 'name' AS "name",
    crew_element ->> 'adult' AS adult,
    crew_element ->> 'gender' AS gender,
    crew_element ->> 'credit_id' AS credit_id,
    crew_element ->> 'department' AS department,
    crew_element ->> 'popularity' AS popularity,
    crew_element ->> 'profile_path' AS profile_path,
    crew_element ->> 'original_name' AS original_name,
    crew_element ->> 'known_for_department' AS known_for_department
FROM {{ source('staging', 'raw_credits')  }} creds,
    LATERAL JSONB_ARRAY_ELEMENTS(creds.crew) AS crew_element
WHERE creds.id IN (SELECT movie_id FROM movies_in_increment)
