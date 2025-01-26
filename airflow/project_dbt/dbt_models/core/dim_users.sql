{{ 
    config(
        materialized='incremental',
        unique_key='user_id'
    ) 
}}

with users as (
    SELECT DISTINCT
        author as "name",
        movie_id,
        author_details ->> 'username' username,
        author_details ->> 'avatar_path' avatar_path
    FROM {{ source('staging', 'raw_reviews') }}
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
    {{ dbt_utils.generate_surrogate_key(['username']) }} as user_id,
    users.name,
    users.username,
    users.avatar_path
FROM users
WHERE users.movie_id IN (SELECT movie_id FROM movies_in_increment)