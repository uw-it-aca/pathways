#!/bin/bash

python3 manage.py migrate
python3 manage.py import_data
