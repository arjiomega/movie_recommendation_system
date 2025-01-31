# Django Dockerfile
FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["sh", "-c", "python ./backend/manage.py makemigrations && python ./backend/manage.py migrate && python ./backend/manage.py runserver 0.0.0.0:8000"]