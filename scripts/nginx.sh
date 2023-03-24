#!/usr/bin/bash

#This command reloads the systemd configuration files
#after copying the Nginx configuration file to the sites-available directory.
#This ensures that any changes made to the configuration file take effect.
sudo systemctl daemon-reload

#This command removes the default Nginx configuration file that comes with
#the installation. This step is not strictly necessary but is done to avoid
#conflicts with the custom configuration file for the Django application.
sudo rm -f /etc/nginx/sites-enabled/default

envsubst < nginx.conf.template > /home/ubuntu/django_project/nginx/nginx.conf

sudo cp /home/ubuntu/django_project/nginx/nginx.conf /etc/nginx/sites-available/simple_django

#This command creates a symbolic link between the sites-available/blog file
#and the sites-enabled directory. This enables the Nginx web server to use
#the blog configuration when serving requests.
sudo ln -s /etc/nginx/sites-available/simple_django /etc/nginx/sites-enabled/

#his command adds the www-data user to the ubuntu group. This is done to allow
#Nginx to access the static files and media files served by the Django application.
sudo gpasswd -a www-data ubuntu

#This command restarts the Nginx web server with the updated configuration.
sudo systemctl restart nginx