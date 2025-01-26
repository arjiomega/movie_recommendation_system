{{ 
    config(
        materialized='incremental',
        unique_key='review_id'
    ) 
}}

with reviews as (
    SELECT
        id as review_id,
        author_details ->> 'username' username,
        movie_id,
        author_details ->> 'rating' rating,
        content as review
    FROM {{ source('staging', 'raw_reviews') }} AS rev
),
movies_in_increment as (
    SELECT mov.movie_id
    FROM {{ ref('dim_movie_info') }} mov
    {% if is_incremental() %}
        WHERE 
            mov.release_date >= '{{ var("start_date") }}' AND -- 2020-01-01
            mov.release_date < '{{ var("end_date") }}' -- 2020-02-01
    {% endif %}
)
SELECT 
    rev.review_id,
    users.user_id,
    rev.movie_id,
    rev.rating,
    rev.review
FROM reviews rev
LEFT JOIN {{ ref('dim_users') }} users
    ON rev.username = users.username
WHERE rev.movie_id IN (SELECT movie_id FROM movies_in_increment)
