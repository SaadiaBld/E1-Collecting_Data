#!/bin/bash

# Créer un fichier de logs pour les erreurs
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="logs/extraction_$TIMESTAMP.log"
mkdir -p logs
exec 2>> "$LOGFILE"  # Rediriger seulement les erreurs vers le log

echo "---------- Lancement : $TIMESTAMP ----------"

# Activer l'environnement virtuel du projet
cd /home/utilisateur/Documents/devia_2425/Certif_2025/E1-collecting_data/c1-extract_data || exit 1
source venv/bin/activate

# Rendre les fichiers bash exécutables
chmod +x scripts/*.sh

# Exécuter les scripts d'extraction
echo "Exécution du script d'extraction des fichiers parquets depuis Azure..."
bash scripts/read_parquet_and_load/run_extractions.sh

# Vérification du driver ODBC
if ! command -v odbcinst &> /dev/null; then
    echo "'odbcinst' non détecté. Installation de unixODBC en cours..."
    sudo apt-get install -y unixodbc 
    echo "unixODBC installé."
fi

echo "Vérification du driver ODBC..."
if odbcinst -q -d | grep -q "ODBC Driver 18 for SQL Server"; then
    echo "Driver ODBC 18 déjà installé."
else
    echo "Driver ODBC 18 manquant. Installation en cours..."
    bash scripts/odbc_install.sh 
    echo "Driver ODBC 18 installé."
fi

# Extraction depuis la base de données Azure
echo "Extraction des données depuis la base de données SQL Server..."
python3 scripts/extract_db_to_csv.py

# Extraction des fichiers CSV
echo "Extraction des fichiers CSV Azure..."
bash scripts/extract_azure_csv_data.sh

# Extraction des fichiers compressés
echo "Extraction des fichiers compressés depuis Azure..."
bash scripts/extract_zip_files.sh

# Extraction des tweets
echo "Extraction des avis clients depuis Twitter..."
python3 ../c1-twitter-api-extract-data/scripts/run_pipeline.py

# Désactiver l'environnement virtuel
deactivate

echo "---------- Fin de l'extraction : $(date +"%Y-%m-%d_%H-%M-%S") ----------"
