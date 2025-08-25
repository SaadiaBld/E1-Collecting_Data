# Projet: E1 - Collecte de Données

## 1. Description Générale

Ce projet centralise plusieurs processus de collecte et de gestion de données provenant de sources variées. Il inclut des scripts pour l'extraction de données depuis des bases de données, des fichiers Parquet, l'API Twitter, ainsi qu'une API pour manipuler les données collectées.

## 2. Installation Globale

Toutes les dépendances Python pour les différents sous-projets sont gérées dans un unique fichier à la racine. Pour les installer, exécutez :

```bash
pip install -r requirements.txt
```

Assurez-vous de vous référer au `README.md` de chaque sous-dossier pour la configuration spécifique (ex: clés d'API, variables d'environnement).

## 3. Structure du Projet

Le projet est divisé en plusieurs modules, chacun avec sa propre documentation détaillée.

### 📁 `c1-extract_data/`

*   **Rôle :** Contient un ensemble de scripts pour des extractions de données générales (ex: depuis des bases de données, fichiers CSV/Parquet, Azure).
*   **Documentation :** [./c1-extract_data/README.md](./c1-extract_data/README.md)

### 📁 `c1-twitter-api-extract-data/`

*   **Rôle :** Un pipeline dédié à la collecte de tweets mentionnant Leroy Merlin, à leur nettoyage et à leur stockage dans une base de données SQLite.
*   **Documentation :** [./c1-twitter-api-extract-data/README.md](./c1-twitter-api-extract-data/README.md)

### 📁 `c5-api_crud/`

*   **Rôle :** Une API (FastAPI) qui expose des points de terminaison CRUD pour gérer les avis clients stockés sur Google BigQuery.
*   **Documentation :** [./c5-api_crud/README.md](./c5-api_crud/README.md)

## 4. Automatisation

Certaines tâches de collecte de données sont automatisées via un script central situé dans `c1-extract_data/cron/automate_all_extractions.sh`. Ce script est conçu pour être exécuté par une tâche cron système.
