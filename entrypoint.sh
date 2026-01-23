#!/bin/sh
# entrypoint.sh - Production entrypoint for Docker + Django

# Exit on error
set -e

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser from environment variables..."
    python manage.py createsuperuser --noinput || echo "ℹ️ Superuser already exists or creation failed"
else
    echo "⚠️ DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD not set, skipping superuser creation"
fi

echo "�🚀 Starting Gunicorn server..."
exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000 --workers 3
