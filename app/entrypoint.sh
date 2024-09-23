#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py collectstatic --noinput
python manage.py add_users
python manage.py add_fake_data
python manage.py add_fake_more_data

exec "$@"