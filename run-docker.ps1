# Script PowerShell pour lancer l'image Docker depuis Docker Hub
# Usage: .\run-docker.ps1

Write-Host "🐳 Récupération de l'image depuis Docker Hub..." -ForegroundColor Cyan
docker pull wilodorico/oc-lettings:latest

Write-Host "`n🚀 Lancement du conteneur..." -ForegroundColor Green
docker run -d `
  --name oc-lettings-prod `
  -p 8000:8000 `
  -e SECRET_KEY="demo-secret-key-change-in-production" `
  -e DEBUG=False `
  -e DJANGO_SETTINGS_MODULE=oc_lettings_site.settings.production `
  -e DJANGO_ENV=production `
  -e DATABASE_URL="sqlite:////app/db.sqlite3" `
  -e ALLOWED_HOSTS="localhost,127.0.0.1" `
  wilodorico/oc-lettings:latest

Write-Host "`n✅ Conteneur lancé avec succès!" -ForegroundColor Green
Write-Host "📍 Application disponible sur: http://localhost:8000" -ForegroundColor Yellow
Write-Host "`nCommandes utiles:" -ForegroundColor Cyan
Write-Host "  - Voir les logs: docker logs oc-lettings-prod -f"
Write-Host "  - Arrêter: docker stop oc-lettings-prod"
Write-Host "  - Supprimer: docker rm oc-lettings-prod"
