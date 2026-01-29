Technologies et langages
========================

Stack technique
---------------

Backend
~~~~~~~

* **Python 3.12.2** : Langage de programmation principal
* **Django 5.2.8** : Framework web
* **Gunicorn 21.2.0** : Serveur WSGI pour la production
* **WhiteNoise 6.6.0** : Gestion des fichiers statiques

Base de données
~~~~~~~~~~~~~~~

* **SQLite 3** : Base de données locale (développement)
* **PostgreSQL** : Base de données production (sur Render)
* **psycopg2-binary 2.9.9** : Adaptateur PostgreSQL

Tests et qualité
~~~~~~~~~~~~~~~~

* **pytest 7.4.3** : Framework de tests
* **pytest-django 4.7.0** : Plugin pytest pour Django
* **pytest-cov 4.1.0** : Couverture de code
* **flake8 6.1.0** : Linter Python

Monitoring
~~~~~~~~~~

* **Sentry SDK 2.19.2** : Monitoring des erreurs et performances

DevOps et déploiement
~~~~~~~~~~~~~~~~~~~~~

* **Docker** : Containerisation de l'application
* **Docker Compose** : Orchestration locale
* **Docker Hub** : Registre d'images (``wilodorico/oc-lettings``)
* **GitHub Actions** : Pipeline CI/CD
* **Render.com** : Hébergement production

Frontend
~~~~~~~~

* **HTML5** : Structure des pages
* **CSS3** : Styles (fichiers statiques)
* **Django Templates** : Moteur de templates

Environnement de développement
-------------------------------

Outils recommandés
~~~~~~~~~~~~~~~~~~

* **Visual Studio Code** : Éditeur de code
* **Git** : Gestion de version
* **Postman/Thunder Client** : Tests API (optionnel)

Extensions VSCode recommandées
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Python (Microsoft)
* Pylance
* Django
* Docker
* GitLens

Structure des dépendances
--------------------------

Le fichier ``requirements.txt`` contient toutes les dépendances :

.. code-block:: text

   Django==5.2.8
   gunicorn==21.2.0
   whitenoise==6.6.0
   psycopg2-binary==2.9.9
   python-dotenv==1.0.0
   dj-database-url==2.1.0
   sentry-sdk==2.19.2
   pytest==7.4.3
   pytest-django==4.7.0
   pytest-cov==4.1.0
   flake8==6.1.0

Variables d'environnement
--------------------------

Configuration locale (``.env``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   SENTRY_DSN=optional-sentry-dsn
   SENTRY_ENVIRONMENT=development

Configuration production (Render)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   SECRET_KEY=production-secret
   DEBUG=False
   DJANGO_SETTINGS_MODULE=oc_lettings_site.settings.production
   DJANGO_ENV=production
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=your-app.onrender.com
   SENTRY_DSN=optional-sentry-dsn

Secrets GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~~

* ``DOCKER_USER_NAME`` : Username Docker Hub
* ``DOCKER_PASSWORD`` : Token Docker Hub
* ``RENDER_DEPLOY_HOOK`` : URL webhook Render

Versions minimales requises
----------------------------

* Python : **3.12+**
* Django : **5.2+**
* Docker : **20.10+**
* Docker Compose : **2.0+**
* Git : **2.30+**
