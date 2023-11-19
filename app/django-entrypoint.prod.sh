#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


# Apply database migrations
echo "Apply database migrations"
python manage.py collectstatic --noinput


# Start configuration
echo "Starting server"
gunicorn config.wsgi --bind 0.0.0.0:8003 --max-requests 100 --max-requests-jitter 20 --log-level warning --timeout 90
