# Pipeline de Collecte de Tweets concernant Leroy Merlin

## 1. Objectif

Ce projet a pour but de collecter, nettoyer et stocker des tweets récents en français qui mentionnent "Leroy Merlin" en relation avec des termes spécifiques comme "livraison", "colis", "commande", etc.

L'objectif est de rassembler des retours clients sur les services de livraison pour une analyse ultérieure.

## 2. Prérequis

*   Python 3
*   Les dépendances Python listées dans le fichier `requirements.txt` à la racine du projet.
*   Un accès à l'API Twitter V2 avec un **Bearer Token** valide.

## 3. Installation et Configuration

1.  **Installer les dépendances :**
    Assurez-vous d'être à la racine du projet (`E1-collecting_data`) et exécutez :
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurer les accès API :**
    a. Créez un fichier nommé `.env` dans le dossier `c1-twitter-api-extract-data/config/`.
    b. Ajoutez votre Bearer Token de l'API Twitter dans ce fichier, comme suit :
    ```
    BEARER_TOKEN="VOTRE_TOKEN_ICI"
    ```

## 4. Utilisation

### Exécution manuelle

Pour lancer le pipeline manuellement, exécutez le script `run_pipeline.py` :

```bash
python3 /home/utilisateur/Documents/devia_2425/Certif_2025/E1-collecting_data/c1-twitter-api-extract-data/scripts/run_pipeline.py
```

Le script va :
1.  Créer la base de données `tweets.db` si elle n'existe pas.
2.  Chercher et charger les nouveaux tweets pertinents.
3.  Nettoyer le texte des tweets et le stocker.

### Automatisation (Cron)

Le lancement de ce pipeline est intégré au script d'automatisation général du projet, situé dans `c1-extract_data/cron/automate_all_extractions.sh`.

Lorsque ce script est exécuté par une tâche `cron`, le pipeline de collecte de tweets est lancé automatiquement.

## 5. Structure du Projet

*   **`data/`** : Contient la base de données `tweets.db` où sont stockées toutes les données collectées.
*   **`config/`** : Destiné à contenir les fichiers de configuration, notamment le fichier `.env` avec les clés d'API.
*   **`scripts/`** :
    *   `database_setup.py` : Initialise la base de données et la table.
    *   `load_tweets.py` : Se connecte à l'API Twitter, cherche et insère les tweets.
    *   `clean_tweets.py` : Nettoie le texte des tweets (suppression des liens, mentions, etc.).
    *   `run_pipeline.py` : Orchestre l'exécution des scripts ci-dessus dans le bon ordre.
    *   `read_data.py` : Script utilitaire pour afficher le contenu de la base de données.
*   **`utils/`** :
    *   `get_user_id.py` : Script utilitaire pour trouver l'ID d'un utilisateur Twitter.
*   **`requirements.txt`** : (À la racine du projet) Fichier listant toutes les dépendances Python nécessaires.
