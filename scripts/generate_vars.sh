#!/usr/bin/env bash

echo generate variables starting...

# remove config.py if it exists
echo remove config.py
sudo rm -f /home/ubuntu/django_project/config.py

# create config.py file
echo generate blank config.py
sudo touch /home/ubuntu/django_project/config.py

# add permission
echo add permission to config.py
sudo chmod 777 /home/ubuntu/django_project/config.py

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

echo Retrieve values from aws parameter store
# Loop over the parameter names and retrieve the values from AWS Parameter Store
for PARAM_NAME in "${PARAM_NAMES[@]}"
do
    echo ${PARAM_NAME}
    PARAM_VALUE=$(aws ssm get-parameters --region ap-northeast-1 --names "${PARAM_NAME}" --with-decryption --query Parameters[0].Value --output text)
    echo ${PARAM_VALUE}
    echo ${PARAM_NAME}=\""${PARAM_VALUE}"\"
    sudo echo ${PARAM_NAME}=\""${PARAM_VALUE}"\" >> /home/ubuntu/django_project/config.py
done