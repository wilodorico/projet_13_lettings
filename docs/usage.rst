Guide d'utilisation
===================

Cette section décrit comment utiliser l'application du point de vue utilisateur et administrateur.

Interface publique
------------------

Page d'accueil
~~~~~~~~~~~~~~

**URL** : http://localhost:8000 (ou https://oc-lettings-bgqe.onrender.com en production)

**Contenu** :

* Titre "Welcome to Holiday Homes"
* Deux liens principaux :
  
  - **Lettings** : Accès à la liste des biens
  - **Profiles** : Accès à la liste des profils

**Cas d'utilisation** : Point d'entrée pour découvrir l'application.

Liste des locations
~~~~~~~~~~~~~~~~~~~

**URL** : ``/lettings/``

**Description** : Affiche tous les biens disponibles à la location.

**Contenu** :

* Liste cliquable des titres de biens
* Lien vers la page d'accueil

**Navigation** :

1. Cliquez sur un titre de bien
2. Vous êtes redirigé vers la page détail du bien

**Exemple de données affichées** :

* "Beautiful Apartment"
* "Charming Cottage"
* "Downtown Studio"

Page détail d'une location
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**URL** : ``/lettings/<id>/``

**Description** : Affiche les informations complètes d'un bien.

**Informations affichées** :

* Titre du bien
* Adresse complète :
  
  - Numéro et rue
  - Ville
  - État (code 2 lettres)
  - Code postal
  - Pays (code ISO)

**Navigation** :

* Lien "Back" : Retour à la liste des locations
* Lien "Home" : Retour à la page d'accueil

**Exemple** :

.. code-block:: text

   Beautiful Apartment
   
   123 Main Street
   Los Angeles, CA 90001
   USA

Liste des profils
~~~~~~~~~~~~~~~~~

**URL** : ``/profiles/``

**Description** : Affiche tous les profils utilisateurs.

**Contenu** :

* Liste cliquable des usernames
* Lien vers la page d'accueil

**Navigation** :

1. Cliquez sur un username
2. Vous êtes redirigé vers la page profil de l'utilisateur

**Exemple de données affichées** :

* "john_doe"
* "jane_smith"
* "bob_wilson"

Page détail d'un profil
~~~~~~~~~~~~~~~~~~~~~~~~

**URL** : ``/profiles/<username>/``

**Description** : Affiche les informations publiques d'un utilisateur.

**Informations affichées** :

* Prénom (First name)
* Nom (Last name)
* Email
* Ville préférée (Favorite city)

**Navigation** :

* Lien "Back" : Retour à la liste des profils
* Lien "Home" : Retour à la page d'accueil

**Exemple** :

.. code-block:: text

   First name: John
   Last name: Doe
   Email: john.doe@example.com
   Favorite city: San Francisco

Erreurs 404
~~~~~~~~~~~

Si vous accédez à une URL inexistante :

* ``/lettings/999/`` : Letting introuvable
* ``/profiles/unknown_user/`` : Profil introuvable

**Comportement** :

* En développement (DEBUG=True) : Page d'erreur Django détaillée
* En production (DEBUG=False) : Page 404 standard

Interface d'administration
---------------------------

Connexion admin
~~~~~~~~~~~~~~~

**URL** : http://localhost:8000/admin

**Credentials** :

* Username : ``admin``
* Password : ``Abc1234!``

**Note** : Ces credentials sont les mêmes en local et en production pour faciliter l'évaluation du projet.

Dashboard admin
~~~~~~~~~~~~~~~

Après connexion, vous accédez au dashboard avec :

**Section Authentication and Authorization** :

* Groups
* Users

**Section Letting** :

* Addresses
* Lettings

**Section Profiles** :

* Profiles

Gestion des utilisateurs
~~~~~~~~~~~~~~~~~~~~~~~~~

**Accès** : Admin > Authentication and Authorization > Users

**Actions disponibles** :

* Créer un nouvel utilisateur
* Modifier un utilisateur existant
* Supprimer un utilisateur
* Changer les permissions
* Définir un mot de passe

**Cas d'utilisation** :

1. Cliquer sur "Add User"
2. Entrer username et password
3. Cliquer "Save and continue editing"
4. Compléter les informations (email, nom, prénom)
5. Définir les permissions si nécessaire
6. Cliquer "Save"

Gestion des profils
~~~~~~~~~~~~~~~~~~~~

**Accès** : Admin > Profiles > Profiles

**Actions disponibles** :

* Créer un profil pour un utilisateur
* Modifier la ville préférée
* Supprimer un profil

**Cas d'utilisation - Créer un profil** :

1. Cliquer sur "Add Profile"
2. Sélectionner un utilisateur dans le dropdown
3. Entrer la ville préférée (optionnel)
4. Cliquer "Save"

**Note** : Un profil doit être lié à un utilisateur existant (relation OneToOne).

Gestion des adresses
~~~~~~~~~~~~~~~~~~~~~

**Accès** : Admin > Letting > Addresses

**Actions disponibles** :

* Créer une nouvelle adresse
* Modifier une adresse existante
* Supprimer une adresse

**Cas d'utilisation - Créer une adresse** :

1. Cliquer sur "Add Address"
2. Remplir les champs :
   
   * Number (ex: 123)
   * Street (ex: Main Street)
   * City (ex: Los Angeles)
   * State (2 lettres, ex: CA)
   * Zip code (ex: 90001)
   * Country ISO code (3 lettres, ex: USA)

3. Cliquer "Save"

**Contraintes de validation** :

* Number : Maximum 9999
* State : Exactement 2 caractères
* Zip code : Maximum 99999
* Country ISO code : Maximum 3 caractères

Gestion des biens (Lettings)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Accès** : Admin > Letting > Lettings

**Actions disponibles** :

* Créer un nouveau bien
* Modifier un bien existant
* Supprimer un bien

**Cas d'utilisation - Créer un bien** :

1. Cliquer sur "Add Letting"
2. Entrer le titre (ex: "Beautiful Apartment")
3. Sélectionner une adresse existante dans le dropdown
4. Cliquer "Save"

**Note** : Vous devez d'abord créer une adresse avant de pouvoir créer un bien.

**Relation cascade** : Si vous supprimez un bien, son adresse associée est également supprimée.

Actions groupées
~~~~~~~~~~~~~~~~

Dans les listes admin, vous pouvez sélectionner plusieurs éléments et effectuer des actions groupées :

* Supprimer les éléments sélectionnés
* Autres actions personnalisées (si configurées)

**Procédure** :

1. Cocher les cases des éléments à traiter
2. Sélectionner l'action dans le dropdown
3. Cliquer "Go"
4. Confirmer l'action

Filtres et recherche
~~~~~~~~~~~~~~~~~~~~

L'interface admin offre des outils de filtrage et recherche :

* **Barre de recherche** : Rechercher par champ texte
* **Filtres latéraux** : Filtrer par date, status, etc.
* **Tri des colonnes** : Cliquer sur l'en-tête pour trier

Cas d'utilisation complets
---------------------------

Scénario 1 : Ajouter un nouveau bien à louer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Objectif** : Le CTO veut ajouter un nouvel appartement au catalogue.

**Étapes** :

1. Se connecter à ``/admin`` avec les credentials admin
2. Aller dans "Addresses" → "Add Address"
3. Créer l'adresse :
   
   * Number: 456
   * Street: Ocean Avenue
   * City: Santa Monica
   * State: CA
   * Zip code: 90401
   * Country: USA

4. Sauvegarder l'adresse
5. Aller dans "Lettings" → "Add Letting"
6. Créer le bien :
   
   * Title: "Beachfront Paradise"
   * Address: Sélectionner "456 Ocean Avenue"

7. Sauvegarder le bien
8. Vérifier sur ``/lettings/`` que le nouveau bien apparaît

Scénario 2 : Créer un profil pour un nouvel utilisateur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Objectif** : Ajouter un nouvel utilisateur avec son profil.

**Étapes** :

1. Se connecter à ``/admin``
2. Aller dans "Users" → "Add User"
3. Créer l'utilisateur :
   
   * Username: alice_wonder
   * Password: (définir un mot de passe sécurisé)

4. Cliquer "Save and continue editing"
5. Compléter les informations :
   
   * First name: Alice
   * Last name: Wonder
   * Email: alice@example.com

6. Sauvegarder
7. Aller dans "Profiles" → "Add Profile"
8. Créer le profil :
   
   * User: alice_wonder
   * Favorite city: New York

9. Sauvegarder
10. Vérifier sur ``/profiles/alice_wonder/`` que le profil s'affiche

Scénario 3 : Consulter les biens disponibles (utilisateur public)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Objectif** : Un visiteur cherche un logement à Los Angeles.

**Étapes** :

1. Accéder à l'application via l'URL publique
2. Cliquer sur "Lettings"
3. Parcourir la liste des biens
4. Cliquer sur "Beautiful Apartment"
5. Vérifier l'adresse complète
6. Noter que c'est à Los Angeles, CA
7. Utiliser "Back" pour revenir à la liste
8. Explorer d'autres options

Scénario 4 : Modifier une adresse existante
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Objectif** : Corriger une erreur dans le code postal.

**Étapes** :

1. Se connecter à ``/admin``
2. Aller dans "Addresses"
3. Chercher l'adresse à corriger
4. Cliquer sur l'adresse
5. Modifier le champ "Zip code"
6. Cliquer "Save"
7. Vérifier le changement sur la page publique du letting associé

Conseils d'utilisation
-----------------------

**Pour les administrateurs** :

* Créez toujours une adresse avant un letting
* Vérifiez les contraintes de validation (taille des champs)
* Utilisez des titres de biens descriptifs
* Complétez tous les champs pour une meilleure expérience utilisateur

**Pour les développeurs** :

* Les changements via l'admin sont immédiats
* Les logs sont disponibles dans ``logs/django.log``
* Utilisez les fixtures pour restaurer des données de test

**Pour les visiteurs** :

* Toutes les données sont publiques (sauf email si non renseigné)
* La navigation est intuitive avec les liens Back/Home
* Pas besoin de compte pour consulter les biens et profils
