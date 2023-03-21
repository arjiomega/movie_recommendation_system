FROM python:3.9-slim-buster

WORKDIR /app

ARG SECRET_KEY
ARG PSQL_NAME
ARG PSQL_USER
ARG PSQL_PASSWORD
ARG PSQL_HOST
ARG PSQL_PORT
ARG TMDB_API_KEY
ARG RS_URL

ENV SECRET_KEY $SECRET_KEY
ENV PSQL_NAME $PSQL_NAME
ENV PSQL_USER $PSQL_USER
ENV PSQL_PASSWORD $PSQL_PASSWORD
ENV PSQL_HOST $PSQL_HOST
ENV PSQL_PORT $PSQL_PORT
ENV TMDB_API_KEY $TMDB_API_KEY
ENV RS_URL $RS_URL


COPY ./simple_app ./simple_app
COPY ./simple_django ./simple_django
COPY requirements.txt .
COPY manage.py .

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn","simple_django.wsgi:application","--bind","0.0.0.0:8000","-w","3","--timeout","600"]