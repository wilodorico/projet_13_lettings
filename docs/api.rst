Interfaces de programmation
===========================

Architecture de l'application
------------------------------

L'application suit l'architecture MVT (Model-View-Template) de Django avec une séparation en applications modulaires.

Structure des URLs
------------------

URL principale (``oc_lettings_site/urls.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   urlpatterns = [
       path('', views.index, name='index'),
       path('lettings/', include('letting.urls')),
       path('profiles/', include('profiles.urls')),
       path('admin/', admin.site.urls),
   ]

**Routes disponibles** :

* ``/`` : Page d'accueil
* ``/lettings/`` : Liste des locations
* ``/profiles/`` : Liste des profils
* ``/admin/`` : Interface d'administration

Application Letting (``letting/urls.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   urlpatterns = [
       path('', views.index, name='letting_index'),
       path('<int:letting_id>/', views.letting, name='letting'),
   ]

**Endpoints** :

* ``GET /lettings/`` : Liste de tous les biens
* ``GET /lettings/<id>/`` : Détails d'un bien spécifique

Application Profiles (``profiles/urls.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   urlpatterns = [
       path('', views.index, name='profiles_index'),
       path('<str:username>/', views.profile, name='profile'),
   ]

**Endpoints** :

* ``GET /profiles/`` : Liste de tous les profils
* ``GET /profiles/<username>/`` : Détails d'un profil spécifique

Vues (Views)
------------

Site principal
~~~~~~~~~~~~~~

**index(request)**

* **URL** : ``/``
* **Méthode** : GET
* **Template** : ``index.html``
* **Contexte** : Aucun
* **Description** : Page d'accueil avec liens vers Lettings et Profiles

Application Letting
~~~~~~~~~~~~~~~~~~~

**index(request)**

* **URL** : ``/lettings/``
* **Méthode** : GET
* **Template** : ``letting/index.html``
* **Contexte** : ``{'lettings_list': Letting.objects.all()}``
* **Description** : Affiche la liste de tous les biens disponibles

**letting(request, letting_id)**

* **URL** : ``/lettings/<int:letting_id>/``
* **Méthode** : GET
* **Template** : ``letting/letting.html``
* **Contexte** : ``{'title': letting.title, 'address': letting.address}``
* **Description** : Affiche les détails d'un bien spécifique
* **Erreur 404** : Si le letting_id n'existe pas

Application Profiles
~~~~~~~~~~~~~~~~~~~~

**index(request)**

* **URL** : ``/profiles/``
* **Méthode** : GET
* **Template** : ``profiles/index.html``
* **Contexte** : ``{'profiles_list': Profile.objects.all()}``
* **Description** : Affiche la liste de tous les profils

**profile(request, username)**

* **URL** : ``/profiles/<str:username>/``
* **Méthode** : GET
* **Template** : ``profiles/profile.html``
* **Contexte** : ``{'profile': profile}``
* **Description** : Affiche le profil d'un utilisateur spécifique
* **Erreur 404** : Si le username n'existe pas

Templates
---------

Structure des templates
~~~~~~~~~~~~~~~~~~~~~~~

::

    templates/
    ├── base.html              # Template de base
    ├── index.html             # Page d'accueil
    ├── letting/
    │   ├── index.html         # Liste des lettings
    │   └── letting.html       # Détail d'un letting
    └── profiles/
        ├── index.html         # Liste des profils
        └── profile.html       # Détail d'un profil

Template de base (``base.html``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contient la structure HTML commune :

* Header avec titre "Holiday Homes"
* Bloc de contenu ``{% block content %}``
* Footer avec copyright

Variables de template disponibles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Letting detail** :

* ``title`` : Titre du bien
* ``address.number`` : Numéro de rue
* ``address.street`` : Nom de rue
* ``address.city`` : Ville
* ``address.state`` : État
* ``address.zip_code`` : Code postal
* ``address.country_iso_code`` : Code pays

**Profile detail** :

* ``profile.user.first_name`` : Prénom
* ``profile.user.last_name`` : Nom
* ``profile.user.email`` : Email
* ``profile.favorite_city`` : Ville préférée

Fichiers statiques
------------------

**Configuration** :

* ``STATIC_URL = '/static/'``
* ``STATIC_ROOT = BASE_DIR / 'staticfiles'``
* WhiteNoise pour le service en production

**Fichier CSS** : ``static/style.css``

**Commande collectstatic** :

.. code-block:: bash

   python manage.py collectstatic --noinput

Gestion des erreurs
-------------------

Page 404 (Not Found)
~~~~~~~~~~~~~~~~~~~~

Déclenchée automatiquement par Django lorsque :

* Un ``letting_id`` n'existe pas
* Un ``username`` n'existe pas

En production (``DEBUG=False``), Django affiche une page 404 personnalisée.

Monitoring Sentry
~~~~~~~~~~~~~~~~~

Toutes les exceptions non gérées sont automatiquement capturées par Sentry (si configuré) :

* Erreurs serveur (500)
* Exceptions Python
* Logs d'erreur

Configuration dans ``settings/production.py`` :

.. code-block:: python

   import sentry_sdk
   
   if SENTRY_DSN:
       sentry_sdk.init(
           dsn=SENTRY_DSN,
           environment=SENTRY_ENVIRONMENT,
           traces_sample_rate=0.1,
       )

Middleware
----------

L'application utilise le middleware Django standard plus WhiteNoise :

.. code-block:: python

   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',  # Fichiers statiques
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

Settings modulaires
-------------------

Configuration séparée en 3 fichiers :

* ``settings/base.py`` : Configuration commune
* ``settings/local.py`` : Configuration développement (DEBUG=True, SQLite)
* ``settings/production.py`` : Configuration production (DEBUG=False, PostgreSQL)

Variables contrôlant le choix :

* ``DJANGO_SETTINGS_MODULE`` : Module settings à charger
* ``DJANGO_ENV`` : Environnement (development/production)

API Admin Django
----------------

L'interface admin est accessible aux superusers sur ``/admin/``.

**Credentials par défaut** :

* Username : ``admin``
* Password : ``Abc1234!``

**Modèles administrables** :

* Letting : Titre, adresse
* Address : Tous les champs d'adresse
* Profile : User, ville préférée
* User : Gestion complète des utilisateurs Django

Logging
-------

Configuration dans ``settings/base.py`` :

* Fichier ``logs/django.log`` : Tous les logs INFO+
* Fichier ``logs/django_errors.log`` : Uniquement les erreurs
* Console : Logs WARNING+ en développement

Format :

.. code-block:: text

   [2026-01-23 10:30:45] INFO Homepage accessed
   [2026-01-23 10:30:50] INFO Lettings index page accessed
