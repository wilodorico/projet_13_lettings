Guide de démarrage rapide
=========================

Cette section vous permet de démarrer rapidement avec l'application en moins de 5 minutes.

Démarrage en 3 étapes
----------------------

1. **Cloner et installer**

.. code-block:: bash

   git clone https://github.com/wilodorico/projet_13_lettings.git
   cd projet_13_lettings
   pip install -r requirements.txt

2. **Configurer l'environnement**

.. code-block:: bash

   cp .env.example .env
   # Éditez .env si nécessaire (les valeurs par défaut fonctionnent)

3. **Lancer le serveur**

.. code-block:: bash

   python manage.py runserver

➡️ Ouvrez http://localhost:8000

Navigation rapide
-----------------

Une fois le serveur lancé, vous pouvez explorer :

* **Page d'accueil** : http://localhost:8000
* **Liste des locations** : http://localhost:8000/lettings/
* **Liste des profils** : http://localhost:8000/profiles/
* **Interface admin** : http://localhost:8000/admin

Credentials admin
-----------------

Pour accéder à l'interface d'administration :

* **Username** : ``admin``
* **Password** : ``Abc1234!``

Tests et qualité
----------------

Exécuter les tests :

.. code-block:: bash

   pytest

Vérifier le linting :

.. code-block:: bash

   flake8

Vérifier la couverture :

.. code-block:: bash

   pytest --cov=. --cov-report=html

Docker (alternative)
--------------------

Si vous préférez Docker :

.. code-block:: bash

   docker-compose up -d

L'application sera disponible sur le même port (8000).

Prochaines étapes
-----------------

* Consultez la section :doc:`usage` pour découvrir les fonctionnalités
* Lisez la section :doc:`deployment` pour déployer en production
* Explorez la section :doc:`api` pour comprendre l'architecture
