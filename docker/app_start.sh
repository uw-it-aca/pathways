#!/bin/bash

python3 manage.py migrate
python3 manage.py import_data
python3 manage.py build_search_index

if [ "$ENV"  = "localdev" ]
then
    # Add any other localdev specific commands here
    :
fi
