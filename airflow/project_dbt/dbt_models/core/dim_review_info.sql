{{ 
    config(
        materialized='incremental',
        unique_key='review_id'
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
	rev.id as review_id,
	rev.created_at,
	rev.updated_at,
	rev.url
FROM {{ source('staging', 'raw_reviews') }} rev
WHERE rev.movie_id IN (SELECT movie_id FROM movies_in_increment)