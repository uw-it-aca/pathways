#!/bin/bash

python3 manage.py import_data
python manage.py build_search_index
