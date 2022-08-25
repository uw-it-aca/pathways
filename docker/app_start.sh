#!/bin/bash

python3 manage.py migrate
python3 manage.py import_data

if [ "$ENV"  = "localdev" ]
then

  python manage.py build_search_index


fi
