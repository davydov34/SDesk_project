#!/bin/bash

#python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn -w 2 SDesk_proj.wsgi:application --bind 0.0.0.0:8000