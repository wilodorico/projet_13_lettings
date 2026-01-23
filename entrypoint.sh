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
    python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, os.getenv('DJANGO_SUPERUSER_PASSWORD'))
    print(f'✅ Superuser created: {username}')
else:
    print(f'ℹ️ Superuser {username} already exists')
EOF
else
    echo "⚠️ DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD not set, skipping superuser creation"
fi

echo "�🚀 Starting Gunicorn server..."
exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000 --workers 3
