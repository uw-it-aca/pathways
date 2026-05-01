#!/bin/bash

if [ "$ENV"  = "localdev" ]
then

  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  source "/app/bin/activate"

  cd /app
  python3 manage.py initialize_person_db
  python3 manage.py migrate
  python3 manage.py import_data
  python3 manage.py build_search_index

fi
