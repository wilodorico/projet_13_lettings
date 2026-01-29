Procédures de déploiement
=========================

Cette section décrit en détail le processus de déploiement automatique et manuel de l'application.

Architecture du déploiement
----------------------------

Vue d'ensemble
~~~~~~~~~~~~~~

Le projet utilise un pipeline CI/CD complet qui automatise :

1. **Tests et linting** sur chaque commit
2. **Construction de l'image Docker** sur la branche main
3. **Push vers Docker Hub** avec tagging automatique
4. **Déploiement sur Render** via webhook

**Schéma du workflow** :

::

    Push GitHub main
          ↓
    [GitHub Actions]
          ↓
    ┌─────┴─────┐
    │   Tests   │  pytest + flake8
    └─────┬─────┘
          ↓
    ┌─────┴─────┐
    │   Build   │  Docker build + tag
    └─────┬─────┘
          ↓
    ┌─────┴─────┐
    │Docker Hub │  Push image
    └─────┬─────┘
          ↓
    ┌─────┴─────┐
    │  Deploy   │  Webhook Render
    └─────┬─────┘
          ↓
    [Render Platform]
          ↓
    Application Live

Pipeline CI/CD
--------------

Fichier de configuration
~~~~~~~~~~~~~~~~~~~~~~~~

**Localisation** : ``.github/workflows/ci-cd.yml``

Le pipeline se compose de 3 jobs séquentiels :

Job 1 : Test (sur toutes les branches)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Déclenchement** : Tous les push et pull requests

**Actions** :

1. Checkout du code
2. Configuration Python 3.12
3. Installation des dépendances
4. **Linting avec Flake8** (max-line-length=119)
5. **Tests avec pytest** 
6. **Vérification de la couverture** (minimum 80%)

**Commandes** :

.. code-block:: bash

   flake8
   pytest --cov=. --cov-fail-under=80

**Condition de succès** : Tous les tests passent ET couverture >= 80%

Job 2 : Build (uniquement sur main)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Déclenchement** : Push sur la branche ``main`` ET si le job Test réussit

**Actions** :

1. Checkout du code
2. Configuration Docker Buildx
3. Login Docker Hub (avec secrets)
4. **Build de l'image Docker**
5. **Tag avec le SHA du commit** (ex: ``main-abc1234``)
6. **Tag avec latest**
7. **Push vers Docker Hub**

**Configuration Docker** :

.. code-block:: yaml

   tags: |
     wilodorico/oc-lettings:${{ github.sha }}
     wilodorico/oc-lettings:latest
   push: true

**Registre** : https://hub.docker.com/r/wilodorico/oc-lettings

Job 3 : Deploy (uniquement sur main)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Déclenchement** : Push sur ``main`` ET si les jobs Test et Build réussissent

**Actions** :

1. **Appel du webhook Render** via curl
2. Render récupère la nouvelle image depuis Docker Hub
3. Render redémarre le service avec la nouvelle image

**Commande** :

.. code-block:: bash

   curl "${{ secrets.RENDER_DEPLOY_HOOK }}"

Configuration des secrets GitHub
---------------------------------

Secrets requis
~~~~~~~~~~~~~~

Dans GitHub : ``Settings → Secrets and variables → Actions``

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Secret
     - Description
   * - ``DOCKER_USER_NAME``
     - Nom d'utilisateur Docker Hub
   * - ``DOCKER_PASSWORD``
     - Token d'accès Docker Hub (pas le mot de passe)
   * - ``RENDER_DEPLOY_HOOK``
     - URL du webhook de déploiement Render

Création du token Docker Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Connexion sur https://hub.docker.com
2. Account Settings → Security → New Access Token
3. Nom : ``github-actions-oc-lettings``
4. Permissions : Read, Write, Delete
5. Copier le token (visible une seule fois)
6. Ajouter dans les secrets GitHub

Configuration Render
--------------------

Créer la base de données PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Dashboard Render → ``New +`` → ``PostgreSQL``
2. Configuration :
   
   * Name : ``oc-lettings-db``
   * Database : (généré automatiquement)
   * Region : Frankfurt (ou proche de vous)
   * Plan : **Free**

3. Attendre la création (1-2 minutes)
4. Noter l'**Internal Database URL**

Créer le service Web
~~~~~~~~~~~~~~~~~~~~

1. Dashboard Render → ``New +`` → ``Web Service``
2. Source : ``Existing Image``
3. Image URL : ``wilodorico/oc-lettings:latest``
4. Configuration :
   
   * Name : ``oc-lettings``
   * Region : Frankfurt (même que la DB)
   * Branch : ``main`` (pour le webhook)
   * Plan : **Free**

5. Cliquer ``Create Web Service``

Configurer les variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dans l'onglet ``Environment`` du service Render :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Valeur
   * - ``SECRET_KEY``
     - Générer une clé secrète Django (50 caractères aléatoires)
   * - ``DEBUG``
     - ``False``
   * - ``DJANGO_SETTINGS_MODULE``
     - ``oc_lettings_site.settings.production``
   * - ``DJANGO_ENV``
     - ``production``
   * - ``DATABASE_URL``
     - (Internal Database URL de votre PostgreSQL)
   * - ``ALLOWED_HOSTS``
     - ``oc-lettings-bgqe.onrender.com`` (votre domaine Render)
   * - ``SENTRY_DSN``
     - (optionnel) Votre DSN Sentry

**Génération de SECRET_KEY** :

.. code-block:: python

   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Récupérer le Deploy Hook
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Service Render → ``Settings`` → ``Deploy Hook``
2. Copier l'URL (format : ``https://api.render.com/deploy/srv-xxx?key=yyy``)
3. Ajouter comme secret ``RENDER_DEPLOY_HOOK`` sur GitHub

Processus de déploiement
-------------------------

Déploiement automatique
~~~~~~~~~~~~~~~~~~~~~~~

**Workflow normal** :

1. Développer sur une branche feature
   
   .. code-block:: bash

      git checkout -b feature/nouvelle-fonctionnalite
      # ... développement ...
      git add .
      git commit -m "feat: Nouvelle fonctionnalité"
      git push origin feature/nouvelle-fonctionnalite

2. Créer une Pull Request sur GitHub
3. Les tests s'exécutent automatiquement (job Test uniquement)
4. Après review, merger vers main
5. **Le déploiement complet se déclenche** :
   
   * Tests → Build → Deploy
   * Durée totale : ~5-10 minutes

6. Vérifier sur https://oc-lettings-bgqe.onrender.com

**Suivi du déploiement** :

* GitHub Actions : https://github.com/wilodorico/projet_13_lettings/actions
* Render Logs : Dashboard → Service → ``Logs``

Déploiement manuel
~~~~~~~~~~~~~~~~~~~

**Sur Render** :

1. Dashboard → Votre service
2. ``Manual Deploy`` → ``Deploy latest commit``
3. Attendre la fin du déploiement

**Cas d'usage** : 

* Forcer un redéploiement après changement de variables d'environnement
* Récupérer d'une erreur de déploiement automatique

Gestion de l'application
-------------------------

Surveillance des logs
~~~~~~~~~~~~~~~~~~~~~

**Logs Render** :

.. code-block:: bash

   # En temps réel sur le dashboard
   Dashboard → Service → Logs

**Logs GitHub Actions** :

.. code-block:: bash

   # Pour chaque workflow
   Repository → Actions → Sélectionner un workflow

**Logs Sentry** (si configuré) :

* Monitoring des erreurs en temps réel
* Alertes par email
* Traces de performance

Commandes utiles
~~~~~~~~~~~~~~~~

**Sur Render (via terminal si accessible en plan payant)** :

.. code-block:: bash

   # Migrations
   python manage.py migrate

   # Collectstatic
   python manage.py collectstatic --noinput

   # Shell Django
   python manage.py shell

**Note** : Le plan gratuit de Render n'a pas accès au Shell. Ces commandes sont exécutées automatiquement dans ``entrypoint.sh``.

Mise à jour des dépendances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Modifier ``requirements.txt`` localement
2. Tester localement :
   
   .. code-block:: bash

      pip install -r requirements.txt
      pytest

3. Commiter et pusher
4. Le déploiement automatique installera les nouvelles dépendances

Rollback en cas de problème
----------------------------

Méthode 1 : Via Git (recommandé)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Revenir au commit précédent
   git revert HEAD
   git push origin main

Le pipeline redéploiera automatiquement la version précédente.

Méthode 2 : Via Render
~~~~~~~~~~~~~~~~~~~~~~~

1. Dashboard → Service → ``Manual Deploy``
2. Sélectionner un commit précédent dans l'historique
3. Déployer

Méthode 3 : Via Docker Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Identifier le tag SHA du commit stable (ex: ``main-abc1234``)
2. Modifier l'image sur Render vers ce tag spécifique
3. Redéployer manuellement

Maintenance et monitoring
--------------------------

Vérifications post-déploiement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Après chaque déploiement, vérifier :

✅ **Page d'accueil** : https://oc-lettings-bgqe.onrender.com  
✅ **Fichiers statiques** : CSS chargé (F12 → Network → Pas d'erreurs 404)  
✅ **Interface admin** : ``/admin`` accessible et stylisée  
✅ **Base de données** : Les données sont présentes  
✅ **Logs Sentry** : Aucune erreur remontée  

Health checks
~~~~~~~~~~~~~

Render effectue automatiquement des health checks :

* Vérifie que le port 8000 répond
* Redémarre le service si nécessaire
* Alerte en cas de downtime

Coûts et limitations
~~~~~~~~~~~~~~~~~~~~

**Plan gratuit Render** :

* 750 heures/mois (suffisant pour 1 application)
* Service s'arrête après 15 minutes d'inactivité
* Premier accès après inactivité : ~30 secondes de démarrage
* 100 GB de bande passante/mois

**Docker Hub gratuit** :

* Repos publics illimités
* 6 heures de build/mois (CI/CD)

**GitHub Actions gratuit** :

* 2000 minutes/mois
* Suffisant pour des dizaines de déploiements

**Total** : 0€/mois pour un projet de formation

Troubleshooting
---------------

Le déploiement échoue sur Render
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Diagnostic** :

1. Vérifier les logs Render
2. Vérifier que toutes les variables d'environnement sont définies
3. Tester l'image Docker localement :
   
   .. code-block:: powershell

      .\\run-docker.ps1

**Solutions courantes** :

* Variable manquante → Ajouter dans Environment
* Image non trouvée → Vérifier le nom d'image (``wilodorico/oc-lettings:latest``)
* Erreur de migration → Vérifier DATABASE_URL

Les fichiers statiques ne se chargent pas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Diagnostic** :

* F12 → Network → Erreurs 404 sur ``/static/``
* Vérifier les logs : ``collectstatic`` s'est-il exécuté ?

**Solutions** :

1. Vérifier ``STATIC_ROOT`` et ``STATIC_URL`` dans ``production.py``
2. Vérifier que WhiteNoise est dans ``MIDDLEWARE``
3. Forcer un redéploiement

L'interface admin est sans style
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Cause** : Fichiers statiques de Django admin non collectés

**Solution** :

Vérifier que ``entrypoint.sh`` exécute bien :

.. code-block:: bash

   python manage.py collectstatic --noinput

Les tests échouent en CI mais pas en local
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Causes possibles** :

* Configuration de test différente
* ``setup.cfg`` pointe vers un mauvais module settings
* Dépendances de test manquantes

**Solution** :

Vérifier ``setup.cfg`` :

.. code-block:: ini

   [tool:pytest]
   DJANGO_SETTINGS_MODULE = oc_lettings_site.settings.local

Le webhook Render ne se déclenche pas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Diagnostic** :

* Vérifier les logs GitHub Actions (job Deploy)
* Vérifier que ``RENDER_DEPLOY_HOOK`` est bien configuré

**Solution** :

Régénérer le Deploy Hook sur Render et mettre à jour le secret GitHub.

Bonnes pratiques
----------------

Pour le développement
~~~~~~~~~~~~~~~~~~~~~

* Toujours créer une branche pour les features
* Tester localement avant de pusher
* Vérifier que les tests passent : ``pytest``
* Vérifier le linting : ``flake8``
* Écrire des messages de commit clairs

Pour le déploiement
~~~~~~~~~~~~~~~~~~~~

* Ne jamais pusher directement sur main sans tests
* Surveiller les logs après déploiement
* Garder les secrets à jour et sécurisés
* Documenter les changements majeurs
* Tester en local avec Docker avant de déployer

Pour la maintenance
~~~~~~~~~~~~~~~~~~~

* Monitorer Sentry régulièrement
* Vérifier les logs Render hebdomadairement
* Mettre à jour les dépendances mensuellement
* Sauvegarder la base de données régulièrement (via pg_dump)
* Documenter les incidents et leurs solutions

Sécurité
~~~~~~~~

* Jamais de credentials dans le code
* Utiliser des variables d'environnement
* ``DEBUG=False`` en production
* Générer une nouvelle ``SECRET_KEY`` pour chaque environnement
* Activer HTTPS (automatique sur Render)
* Configurer ``ALLOWED_HOSTS`` strictement
