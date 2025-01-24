FROM apache/airflow:2.10.4

# Directories
COPY ../keys ./keys

# Individual Files 
COPY ./airflow/requirements.txt \
    ./.env \
    ./airflow/project_dbt/dbt_project.yml \
    ./airflow/project_dbt/packages.yml \
    ./airflow/project_dbt/profiles.yml \
    ./

RUN pip3.12 install --upgrade pip setuptools wheel \
    && pip3.12 install --no-cache-dir -r requirements.txt

RUN dbt deps