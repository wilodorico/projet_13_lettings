#!/bin/sh
# entrypoint.sh - Production entrypoint for Docker + Django

# Exit on error
set -e

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "�🚀 Starting Gunicorn server..."
exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000 --workers 3
