## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure
- Compte Sentry (gratuit) pour la journalisation des erreurs

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- Copier le fichier `.env.example` vers `.env` et configurer les variables (voir section Configuration Sentry)
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement avec Docker

### Prérequis

- Docker Desktop installé et démarré
- Docker Compose (inclus avec Docker Desktop)
- Fichier `.env` configuré (voir section Configuration)

### Configuration initiale

1. **Copier et configurer les variables d'environnement**
   ```bash
   # Copier le fichier d'exemple
   cp .env.example .env
   
   # Éditer .env et configurer vos variables
   # Notamment : SENTRY_DSN, SECRET_KEY, DEBUG, etc.
   ```

### Démarrage de l'application

#### Premier lancement
```bash
# Construire l'image et démarrer le conteneur
docker-compose up --build

# Ou en arrière-plan (recommandé)
docker-compose up -d --build
```

#### Lancements suivants
```bash
# Démarrage simple (sans rebuild)
docker-compose up

# En arrière-plan
docker-compose up -d
```

**Accès à l'application** : `http://localhost:8000`

### Gestion du conteneur

#### Arrêter et supprimer les conteneurs
```bash
# Arrête et supprime les conteneurs (les volumes et images sont conservés)
docker-compose down

# Avec suppression des volumes (⚠️ perte de données)
docker-compose down -v
```

#### Arrêter sans supprimer
```bash
# Pause le conteneur (peut être redémarré avec docker-compose start)
docker-compose stop

# Redémarrer après un stop
docker-compose start
```

#### Redémarrer le conteneur
```bash
docker-compose restart
```

### Commandes utiles

#### Voir les logs
```bash
# Logs en temps réel (mode attaché)
docker-compose logs -f

# Logs uniquement du service web
docker-compose logs -f web

# Dernières 100 lignes
docker-compose logs --tail=100
```

#### Exécuter des commandes dans le conteneur
```bash
# Lancer des commandes Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Lancer les tests
docker-compose exec web pytest

# Accéder au shell Python Django
docker-compose exec web python manage.py shell

# Accéder au shell bash du conteneur
docker-compose exec web bash
```

#### Vérifier l'état
```bash
# Voir les conteneurs en cours d'exécution
docker-compose ps

# Voir les logs d'erreurs
docker-compose logs web | grep -i error
```

### Utilisation sans Docker Compose

Si vous préférez utiliser Docker directement :

```bash
# Construire l'image
docker build -t oc-lettings:latest .

# Lancer le conteneur avec montage de volume
docker run -d \
  -p 8000:8000 \
  -v "$(pwd):/app" \
  --env-file .env \
  --name oc-lettings-web \
  oc-lettings:latest

# Arrêter et supprimer
docker stop oc-lettings-web
docker rm oc-lettings-web
```

### Persistance des données

La base de données SQLite est **persistante** grâce au volume monté :
```yaml
volumes:
  - .:/app  # Le répertoire local est monté dans /app du conteneur
```

Le fichier `oc-lettings-site.sqlite3` reste sur votre machine locale et survit aux `docker-compose down`.

### Résolution de problèmes

#### Le conteneur ne démarre pas
```bash
# Vérifier les logs
docker-compose logs web

# Reconstruire complètement
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Port 8000 déjà utilisé
```bash
# Modifier le port dans docker-compose.yml
ports:
  - "8001:8000"  # Utiliser le port 8001 au lieu de 8000
```

#### Problèmes de permissions (Linux/Mac)
```bash
# Ajuster les permissions du fichier SQLite
chmod 664 oc-lettings-site.sqlite3
```

## Configuration Sentry

Sentry est configuré pour capturer automatiquement les erreurs et surveiller les performances de l'application.

### Configuration requise

1. **Créer un compte Sentry**
   - Rendez-vous sur [sentry.io](https://sentry.io/)
   - Créez un compte gratuit
   - Créez un nouveau projet Django
   - Récupérez votre DSN depuis Settings > Projects > Your Project > Client Keys (DSN)

2. **Configurer les variables d'environnement**
   ```bash
   # Copier le fichier d'exemple
   cp .env.example .env
   
   # Éditer .env et ajouter vos informations Sentry
   SENTRY_DSN=https://your-actual-dsn@sentry.io/project-id
   SENTRY_ENVIRONMENT=development  # ou production, staging, etc.
   ```

### Fonctionnement

Sentry capturera automatiquement :
- ✅ Toutes les exceptions non gérées
- ✅ Les erreurs HTTP 500
- ✅ Les performances des transactions (requêtes HTTP)
- ✅ Les logs d'erreurs Django

Les logs sont également enregistrés localement dans le dossier `logs/` :
- `django.log` : Tous les logs INFO et supérieurs
- `django_errors.log` : Uniquement les erreurs (ERROR et CRITICAL)
