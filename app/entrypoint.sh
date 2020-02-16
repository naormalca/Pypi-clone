#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
#TODO: execute this script only at the first time
python my_pypi/bin/load_data.py
python my_pypi/app.py

exec "$@"