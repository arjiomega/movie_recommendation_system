{{ 
    config(
        materialized='incremental',
        unique_key='company_id'
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
    production_company_element ->> 'id' AS company_id,
    production_company_element ->> 'origin_country' AS country_id,
    production_company_element ->> 'name' AS company_name,
    production_company_element ->> 'logo_path' AS logo_path
FROM {{ source('staging', 'raw_movies')  }} mov,
     LATERAL JSONB_ARRAY_ELEMENTS(mov.production_companies) AS production_company_element
WHERE mov.id IN (SELECT movie_id FROM movies_in_increment)
