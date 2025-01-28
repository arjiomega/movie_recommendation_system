{{ 
    config(
        materialized='incremental',
        unique_key='movie_id'
    ) 
}}

SELECT DISTINCT
    mov.id as movie_id,
    mov.title,
    mov.original_title,
    mov.release_date,
    mov.original_language,
    mov.adult,
    mov.video,
    mov.backdrop_path,
    mov.poster_path,
    mov.overview,
    mov.homepage,
    mov.status,
    mov.tagline
FROM {{ source('staging', 'raw_movies') }} mov

{% if is_incremental() %}
    WHERE 
        mov.release_date >= '{{ var("start_date") }}' AND -- 2020-01-01
        mov.release_date < '{{ var("end_date") }}' -- 2020-02-01
{% endif %}