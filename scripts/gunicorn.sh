#!/usr/bin/bash

# start automatically on boot (ensures app always running)
sudo cp /home/ubuntu/django_project/gunicorn/gunicorn.socket  /etc/systemd/system/gunicorn.socket
sudo cp /home/ubuntu/django_project/gunicorn/gunicorn.service  /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service