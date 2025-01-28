{{ 
    config(
        materialized='incremental',
        unique_key='movie_id'
    ) 
}}

with review_counts as (
    SELECT movie_id, COUNT(*) AS total_reviews FROM {{ source('staging', 'raw_reviews') }}
    GROUP BY movie_id
    ORDER BY total_reviews DESC
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
SELECT DISTINCT
    mov.id as movie_id,
    mov.vote_count,
    mov.vote_average,
    mov.popularity,
    review_counts.total_reviews,
    mov.budget,
    mov.revenue,
    mov.runtime
FROM {{ source('staging', 'raw_movies') }} AS mov
LEFT JOIN review_counts
    ON mov.id = review_counts.movie_id
WHERE mov.id IN (SELECT movie_id FROM movies_in_increment)
