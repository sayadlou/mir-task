#!/bin/bash

#echo "Create migrations"
python manage.py makemigrations --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "collecting static files"
python manage.py collectstatic --noinput

# Run configuration
python manage.py runserver 0.0.0.0:8003
