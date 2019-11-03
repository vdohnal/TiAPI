#!/bin/sh

cd /code
while ! pg_isready -h "db" -p ${DB_PORT} > /dev/null 2> /dev/null; do
    echo "Connecting to 'db' Failed"
    sleep 1
  done
#python manage.py migrate --noinput || exit 1
echo "Makemigrations"
python manage.py makemigrations --noinput  || exit 1
echo "Migrate"
python manage.py migrate --noinput || exit 1
echo "Collectstatic"
python manage.py collectstatic --noinput
echo "Createsuperuser"
python manage.py createsuperuser2 --username ${ADMIN_USERNAME} --password ${ADMIN_PASSWORD} --noinput --email ${ADMIN_EMAIL}
echo "Gunicorn"
gunicorn -b 0.0.0.0:8000 TiAPI_project.wsgi:application