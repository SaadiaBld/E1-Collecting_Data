# API CRUD pour les Avis Clients (BigQuery)

## 1. Objectif

Cette application fournit une API RESTful (basée sur FastAPI) pour gérer des avis clients (`reviews`) et leurs analyses de sujets (`topics`) stockés dans une base de données Google BigQuery.

Elle expose des points de terminaison (endpoints) pour les opérations CRUD (Create, Read, Update, Delete) sur les données.

## 2. Prérequis

*   Python 3
*   Les dépendances Python listées dans le fichier `requirements.txt` à la racine du projet (notamment `fastapi`, `uvicorn`, `google-cloud-bigquery`).
*   Un projet Google Cloud avec l'API BigQuery activée.
*   Un compte de service Google Cloud avec les permissions nécessaires pour lire et écrire dans BigQuery.

## 3. Installation et Configuration

1.  **Installer les dépendances :**
    Depuis la racine du projet (`E1-collecting_data`), exécutez :
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurer les accès Google Cloud :**
    a. Placez le fichier de clés JSON de votre compte de service dans le dossier `c5-api_crud/config/`.
    b. Créez un fichier nommé `.env` dans ce même dossier `config/`.
    c. Ajoutez les variables suivantes dans le fichier `.env` :
    ```
    # ID de votre projet Google Cloud
    PROJECT_ID="votre-projet-gcp-id"

    # Chemin relatif vers votre fichier de clés depuis le dossier c5-api_crud/
    GOOGLE_APPLICATION_CREDENTIALS="config/votre-fichier-de-cles.json"
    ```

## 4. Utilisation

Pour lancer le serveur de l'API, placez-vous dans le dossier `c5-api_crud/` et exécutez la commande suivante :

```bash
uvicorn main:app --reload
```

*   `main`: Fait référence au fichier `main.py`.
*   `app`: L'objet FastAPI créé dans `main.py`.
*   `--reload`: Le serveur redémarrera automatiquement après chaque modification du code.

Une fois le serveur lancé, l'API est accessible à l'adresse `http://127.0.0.1:8000`.

La documentation interactive de l'API (générée par Swagger UI) est disponible à l'adresse : **`http://127.0.0.1:8000/docs`**.

## 5. Endpoints de l'API

*   `GET /reviews`: Récupère la liste de tous les avis.
*   `POST /reviews`: Crée un nouvel avis.
*   `GET /reviews/{review_id}`: Récupère un avis spécifique et les analyses de sujets associées.
*   `PUT /reviews/{review_id}`: Met à jour le contenu d'un avis spécifique.
*   `DELETE /reviews/{review_id}`: Supprime un avis et ses analyses associées.
*   `GET /topics`: Récupère la liste de tous les sujets possibles.

## 6. Structure du Projet

*   **`main.py`**: Le point d'entrée de l'application FastAPI. Définit les routes de l'API et gère les requêtes HTTP.
*   **`models.py`**: Contient les modèles de données Pydantic. Ces modèles valident les données des requêtes entrantes et structurent les réponses sortantes.
*   **`bigquery_service.py`**: La couche de service. Contient toute la logique métier pour interagir avec Google BigQuery (lire, insérer, mettre à jour, supprimer des données).
*   **`config/`**: Dossier destiné à contenir les fichiers de configuration, comme le `.env` et les clés d'accès GCP.
