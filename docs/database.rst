Structure de la base de données
================================

Schéma général
--------------

L'application utilise 3 modèles principaux organisés dans 2 applications Django :

* **Application ``letting``** : Gestion des biens immobiliers
* **Application ``profiles``** : Gestion des profils utilisateurs
* **Django ``auth``** : Modèle User standard de Django

Modèle Address
--------------

**Application** : ``letting``

**Description** : Représente une adresse physique complète.

**Champs** :

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - ``id``
     - AutoField
     - Clé primaire auto-incrémentée
   * - ``number``
     - PositiveIntegerField
     - Numéro de rue (max 9999)
   * - ``street``
     - CharField(64)
     - Nom de la rue
   * - ``city``
     - CharField(64)
     - Ville
   * - ``state``
     - CharField(2)
     - Code état US (ex: CA, NY)
   * - ``zip_code``
     - PositiveIntegerField
     - Code postal (max 99999)
   * - ``country_iso_code``
     - CharField(3)
     - Code pays ISO (ex: USA)

**Contraintes** :

* ``number`` : Valeur maximale 9999
* ``state`` : Exactement 2 caractères
* ``zip_code`` : Valeur maximale 99999
* ``country_iso_code`` : Maximum 3 caractères

**Méthode** :

* ``__str__()`` : Retourne le numéro et le nom de la rue

**Exemple** :

.. code-block:: python

   address = Address.objects.create(
       number=123,
       street="Main Street",
       city="Los Angeles",
       state="CA",
       zip_code=90001,
       country_iso_code="USA"
   )
   print(address)  # "123 Main Street"

Modèle Letting
--------------

**Application** : ``letting``

**Description** : Représente un bien immobilier disponible à la location.

**Champs** :

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - ``id``
     - AutoField
     - Clé primaire auto-incrémentée
   * - ``title``
     - CharField(256)
     - Titre/nom du bien
   * - ``address``
     - OneToOneField(Address)
     - Adresse du bien (relation 1:1)

**Relations** :

* **OneToOne avec Address** : Chaque bien a une adresse unique, suppression en cascade

**Contraintes** :

* ``title`` : Maximum 256 caractères
* ``address`` : Clé étrangère obligatoire avec ``on_delete=CASCADE``

**Méthode** :

* ``__str__()`` : Retourne le titre du bien

**Exemple** :

.. code-block:: python

   letting = Letting.objects.create(
       title="Beautiful Apartment",
       address=address
   )
   print(letting)  # "Beautiful Apartment"
   print(letting.address.city)  # "Los Angeles"

Modèle Profile
--------------

**Application** : ``profiles``

**Description** : Profil utilisateur étendu lié au modèle User de Django.

**Champs** :

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - ``id``
     - AutoField
     - Clé primaire auto-incrémentée
   * - ``user``
     - OneToOneField(User)
     - Utilisateur Django associé
   * - ``favorite_city``
     - CharField(64)
     - Ville préférée de l'utilisateur

**Relations** :

* **OneToOne avec User** : Chaque profil est lié à un utilisateur Django unique

**Contraintes** :

* ``favorite_city`` : Maximum 64 caractères, peut être vide (``blank=True``)
* ``user`` : Clé étrangère obligatoire avec ``on_delete=CASCADE``

**Méthode** :

* ``__str__()`` : Retourne le username de l'utilisateur

**Exemple** :

.. code-block:: python

   from django.contrib.auth.models import User
   
   user = User.objects.create_user(
       username='john_doe',
       email='john@example.com'
   )
   
   profile = Profile.objects.create(
       user=user,
       favorite_city='San Francisco'
   )
   
   print(profile)  # "john_doe"
   print(profile.favorite_city)  # "San Francisco"

Diagramme de relations
-----------------------

::

    ┌──────────────┐
    │     User     │
    │  (Django)    │
    └──────┬───────┘
           │ 1:1
           │
    ┌──────▼───────┐
    │   Profile    │
    │              │
    │ favorite_city│
    └──────────────┘

    ┌──────────────┐       ┌──────────────┐
    │   Letting    │  1:1  │   Address    │
    │              │◄──────│              │
    │ title        │       │ number       │
    └──────────────┘       │ street       │
                           │ city         │
                           │ state        │
                           │ zip_code     │
                           │ country_iso  │
                           └──────────────┘

Migrations
----------

Les migrations Django se trouvent dans :

* ``letting/migrations/`` : Modèles Letting et Address
* ``profiles/migrations/`` : Modèle Profile
* ``oc_lettings_site/migrations/`` : Migrations legacy (site principal)

Commandes utiles
----------------

Créer une nouvelle migration :

.. code-block:: bash

   python manage.py makemigrations

Appliquer les migrations :

.. code-block:: bash

   python manage.py migrate

Afficher l'état des migrations :

.. code-block:: bash

   python manage.py showmigrations

Revenir en arrière :

.. code-block:: bash

   python manage.py migrate letting 0001

Charger les données de test :

.. code-block:: bash

   python manage.py loaddata fixtures.json

Accès admin
-----------

Tous les modèles sont enregistrés dans l'interface Django Admin :

* **Lettings** : http://localhost:8000/admin/letting/letting/
* **Addresses** : http://localhost:8000/admin/letting/address/
* **Profiles** : http://localhost:8000/admin/profiles/profile/
* **Users** : http://localhost:8000/admin/auth/user/

Base de données en production
------------------------------

**Développement** : SQLite (``oc-lettings-site.sqlite3``)

**Production** : PostgreSQL sur Render

La connexion est gérée automatiquement via ``DATABASE_URL`` et ``dj-database-url``.
