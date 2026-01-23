#!/bin/bash
# Script bash pour lancer l'image Docker depuis Docker Hub
# Usage: ./run-docker.sh

echo "🐳 Récupération de l'image depuis Docker Hub..."
docker pull wilodorico/oc-lettings:latest

echo ""
echo "🚀 Lancement du conteneur..."
docker run -d \
  --name oc-lettings-prod \
  -p 8000:8000 \
  -e SECRET_KEY="demo-secret-key-change-in-production" \
  -e DEBUG=False \
  -e DJANGO_SETTINGS_MODULE=oc_lettings_site.settings.production \
  -e DJANGO_ENV=production \
  -e DATABASE_URL="sqlite:////app/db.sqlite3" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  wilodorico/oc-lettings:latest

echo ""
echo "✅ Conteneur lancé avec succès!"
echo "📍 Application disponible sur: http://localhost:8000"
echo ""
echo "Commandes utiles:"
echo "  - Voir les logs: docker logs oc-lettings-prod -f"
echo "  - Arrêter: docker stop oc-lettings-prod"
echo "  - Supprimer: docker rm oc-lettings-prod"
