#!/bin/sh

which poetry
python manage.py collectstatic --noinput
python manage.py migrate --noinput
uwsgi --ini /app/config/server/uwsgi.ini
