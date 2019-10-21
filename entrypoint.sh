#!/bin/sh

cd /code
python manage.py makemigrations
until python manage.py migrate; do
  sleep 2
  echo "Retry!";
done
python manage.py collectstatic --noinput
gunicorn -b 0.0.0.0:8000 TiAPI_project.wsgi:application