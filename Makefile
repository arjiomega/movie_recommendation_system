SHELL = /bin/bash


include .env
export

# Build and run docker image
.ONESHELL:
.PHONY: rundocker
rundocker:
	sudo docker build -t django_image \
	--build-arg SECRET_KEY=${SECRET_KEY} \
	--build-arg PSQL_NAME=${PSQL_NAME} \
	--build-arg PSQL_USER=${PSQL_USER} \
	--build-arg PSQL_PASSWORD=${PSQL_PASSWORD} \
	--build-arg PSQL_HOST=${PSQL_HOST} \
	--build-arg PSQL_PORT=${PSQL_PORT} \
	--build-arg TMDB_API_KEY=${TMDB_API_KEY} \
	--build-arg RS_URL=${RS_URL} --no-cache .
	sudo docker run -p 8000:8000 django_image

