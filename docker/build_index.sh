#!/bin/bash

source bin/activate
python3 manage.py import_data
python3 manage.py build_search_index
