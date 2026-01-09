#!/bin/sh
# entrypoint.sh - pour Docker + Django

# Quitte en cas d'erreur
set -e

# echo "🔄 Appliquer les migrations..."
# python manage.py migrate

echo "🚀 Lancement du serveur..."
# En dev, runserver. En prod, on remplacera par gunicorn
exec "$@"
