# Data Extraction 

# Contexte du projet

Adventure Works, leader dans la vente de vélos et d’équipements cyclistes, explore le potentiel du machine learning multimodal pour optimiser les recommandations produits et mieux comprendre ses clients. L'objectif est de combiner des données textuelles (avis clients, descriptions produits) et visuelles (images des produits) afin de développer un modèle capable d'exploiter ces différentes modalités.

Ce projet est une preuve de concept (POC) visant à tester la faisabilité de l'extraction et de la gestion de données multisources. 
L'extraction de données est réalisée à partir de :

    Un fichier de données plat (CSV).
    Une base de données relationnelle hébergée dans le cloud (Azure MySQL).
    Un système big data.

### Prérequis

    Environnement Python :
        Python 3.8 ou plus récent.
        Installer les dépendances avec :

    pip install -r requirements.txt

Accès aux sources de données :

    Configurer les fichiers d'accès (par exemple, .env) pour les connexions aux bases de données.

### Comment utiliser le script extract_azure_csv_data.sh ? 

Ce script permet de récupérer automatiquement tous les fichiers `.csv` depuis un conteneur Azure Blob Storage dans un dossier local `nlp_data`.

#### Prérequis :
- Avoir installé [`azcopy`](https://learn.microsoft.com/fr-fr/azure/storage/common/storage-use-azcopy-v10)
- Avoir installé [Azure CLI](https://learn.microsoft.com/fr-fr/cli/azure/install-azure-cli)
- Avoir un accès au compte de stockage Azure (`az login`)

#### Lancer le script :
```bash
chmod +x scripts/azure_files.sh
./scripts/azure_files.sh
``` 

#### Comment utiliser le script extract_db_to_csv.py:
Le script se connecte à une base Azure SQL via ODBC, extrait toutes les données des tables ciblées (`Sales`, `Production`, `Person`) et les sauvegarde dans des fichiers CSV dans le dossier `db_files/`.
Pour utiliser ce script, installer le pilote ODBC 18 de microsoft. Le script odbc_install configure les depots microsoft et installe le pilote.

```bash
chmod +x scripts/odbc_install.sh
bash scripts/odbc_install.sh
```
Ensuite on peut executer le script pour extraire les données depuis la db. 

#### Lancer le script :
```bash
python scripts/extract_sql_to_csv.py
```

### Comment telecharger le contenu de fichiers parquet ? 
Ce module permet d’extraire automatiquement des fichiers .parquet stockés dans Azure Blob Storage, puis de générer localement les images et métadonnées associées.

*Étapes automatisées :

    Génération d’URLs SAS sécurisées pour accéder aux fichiers .parquet (via generate_sas_parquet_urls.sh)

    Téléchargement des fichiers en local en reproduisant la structure des dossiers Azure (via download_parquet_files.sh)

    Extraction des images et métadonnées à partir des fichiers .parquet (via read_parquet.py)

    Orchestration complète des étapes via un seul script : run_extractions.sh

#### Lancer le script :
```bash
chmod +x scripts/*sh
python scripts/read_parquet_and_load/run_extractions.sh
```