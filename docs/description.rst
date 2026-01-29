Description du projet
=====================

Présentation générale
---------------------

Orange County Lettings est une application web Django permettant de gérer des locations immobilières et des profils utilisateurs dans le comté d'Orange, Californie.

L'application permet de :

* Consulter la liste des biens disponibles à la location
* Afficher les détails de chaque bien (adresse complète)
* Gérer les profils des utilisateurs
* Administrer les données via l'interface Django Admin

Objectifs du projet
-------------------

Ce projet a été développé dans le cadre d'une refonte technique visant à :

1. **Modulariser l'architecture** : Séparation du code monolithique en applications Django distinctes (``letting``, ``profiles``)
2. **Améliorer la qualité** : Mise en place de tests unitaires avec une couverture >80%
3. **Automatiser le déploiement** : Pipeline CI/CD complet avec GitHub Actions
4. **Containeriser l'application** : Utilisation de Docker pour la portabilité
5. **Déployer en production** : Hébergement sur Render.com avec PostgreSQL

Contexte métier
---------------

Le site est utilisé par Orange County Lettings pour présenter leur catalogue de biens immobiliers. 
L'interface d'administration est fréquemment utilisée par le CTO pour gérer les données, d'où l'importance de son apparence et de sa facilité d'utilisation.

URL de production
-----------------

L'application est accessible publiquement à l'adresse :

https://oc-lettings-bgqe.onrender.com
