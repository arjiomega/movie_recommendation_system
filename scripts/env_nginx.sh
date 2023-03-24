#!/usr/bin/env bash

export ELASTIC_IP=$ELASTIC_IP
envsubst < nginx.conf.template > /home/ubuntu/django_project/nginx/nginx.conf