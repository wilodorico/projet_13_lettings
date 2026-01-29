#!/bin/sh
# entrypoint.sh - Production entrypoint for Docker + Django

# Exit on error
set -e

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Load fixtures if database is empty (demo data)
if [ -f "fixtures.json" ]; then
    echo "📂 Checking if demo data needs to be loaded..."
    python manage.py shell -c "from letting.models import Letting; print('skip' if Letting.objects.exists() else 'load')" | grep -q "load" && {
        echo "📥 Loading demo data from fixtures..."
        python manage.py loaddata fixtures.json
        echo "✅ Demo data loaded successfully"
    } || echo "ℹ️ Demo data already exists, skipping"
fi


echo "�🚀 Starting Gunicorn server..."
exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000 --workers 3
