#!/bin/sh
set -e

echo "Waiting for database..."
until nc -z db 5432; do
  sleep 1
done
echo "Database started"

echo "Running data migrator..."
python /app/Scripts/migrator.py

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
