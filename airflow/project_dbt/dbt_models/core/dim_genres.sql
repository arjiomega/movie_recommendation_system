{{ 
    config(
        materialized='table',
    ) 
}}

SELECT 
    id as genre_id,
    name as genre_name
FROM {{ source('staging', 'raw_genres') }} AS genres