#!/bin/bash

python3 manage.py migrate
python3 manage.py import_data

if [ "$ENV"  = "localdev" ]
then

  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  source "/app/bin/activate"

  cd /app
  python manage.py migrate
  python manage.py loaddata person employee term major student adviser transfer transcript hold degree sport
  python manage.py build_search_index

fi
