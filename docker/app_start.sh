source "/app/bin/activate"

cd /app
python manage.py migrate
python manage.py import_data
