#!/usr/bin/env bash

rm -f /home/ubuntu/django_project/config.py

# Array of parameter names
PARAM_NAMES=(
    SECRET_KEY
    PSQL_NAME
    PSQL_USER
    PSQL_PASSWORD
    PSQL_HOST
    PSQL_PORT
    TMDB_API_KEY
    RS_URL
)

# Loop over the parameter names and retrieve the values from AWS Parameter Store
for PARAM_NAME in "${PARAM_NAMES[@]}"
do
    PARAM_VALUE=$(aws ssm get-parameters --region ap-northeast-1 --names "${PARAM_NAME}" --with-decryption --query Parameters[0].Value)
    echo ${PARAM_NAME}=\""${PARAM_VALUE}"\"
    echo ${PARAM_NAME}=\""${PARAM_VALUE}"\" >> /home/ubuntu/django_project/config.py
done