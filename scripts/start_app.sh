#!/usr/bin/bash

#This command uses the sed tool to search for an empty list ([]) in the settings.py
#file and replace it with a list containing the IP address of the server. This is
#typically done to allow the Django application to accept requests from this IP address.
sed -i 's/\[]/\["13.113.126.172"]/' /home/ubuntu/django_project/simple_django/settings.py

#This command applies any database migrations that have not yet been applied to the database.
#python manage.py migrate

#This command generates new migration files for any changes to the database schema.
#python manage.py makemigrations


#This command collects all the static files used by the Django application and puts
#them in a single directory.
python3 manage.py collectstatic

sudo service gunicorn restart
sudo service nginx restart