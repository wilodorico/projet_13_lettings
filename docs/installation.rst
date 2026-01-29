Installation
============

Prérequis
---------

Avant de commencer, assurez-vous d'avoir installé :

* Python 3.12 ou supérieur
* Git
* Docker Desktop (pour l'exécution en conteneur)
* Un compte GitHub

Cloner le repository
--------------------

.. code-block:: bash

   git clone https://github.com/wilodorico/projet_13_lettings.git
   cd projet_13_lettings

Créer l'environnement virtuel
------------------------------

**Sur Windows** :

.. code-block:: powershell

   python -m venv venv
   .\venv\Scripts\Activate.ps1

**Sur macOS/Linux** :

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate

Installer les dépendances
--------------------------

.. code-block:: bash

   pip install -r requirements.txt

Configuration des variables d'environnement
--------------------------------------------

1. Copiez le fichier d'exemple :

.. code-block:: bash

   cp .env.example .env

2. Éditez le fichier ``.env`` et configurez les variables :

.. code-block:: bash

   # Django
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Sentry (optionnel)
   SENTRY_DSN=your-sentry-dsn
   SENTRY_ENVIRONMENT=development

Configuration de Sentry
------------------------

Pour activer le monitoring des erreurs avec Sentry :

1. Créez un compte sur https://sentry.io
2. Créez un nouveau projet Django
3. Copiez votre DSN dans le fichier ``.env``

Sentry est optionnel et l'application fonctionne sans.

Initialiser la base de données
-------------------------------

La base de données SQLite est déjà fournie avec des données de test. 
Si vous souhaitez repartir de zéro :

.. code-block:: bash

   python manage.py migrate
   python manage.py loaddata fixtures.json

Vérification de l'installation
-------------------------------

Lancez le serveur de développement :

.. code-block:: bash

   python manage.py runserver

Accédez à http://localhost:8000 dans votre navigateur. 
Vous devriez voir la page d'accueil d'OC Lettings.

Installation avec Docker
-------------------------

Pour exécuter l'application dans un conteneur Docker :

.. code-block:: bash

   docker-compose up --build

L'application sera accessible sur http://localhost:8000
