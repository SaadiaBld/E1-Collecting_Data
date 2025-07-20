#!/bin/bash
# Script pour télécharger des fichiers Parquet depuis Azure Blob Storage, à partir des urls générées par generate_sas_parquet_urls.sh
URLS_FILE="data/extraction_from_parquet/urls.txt"
DEST_DIR="data/extraction_from_parquet"
mkdir -p data/extraction_from_parquet

if [ ! -f "$URLS_FILE" ]; then
    echo "Fichier d'URL introuvable : $URLS_FILE"
    exit 1
fi

mkdir -p "$DEST_DIR"

while read -r URL; do
    FILE_NAME=$(basename "${URL%%\?*}")
    wget "$URL" -O "$DEST_DIR/$FILE_NAME"
done < "$URLS_FILE"

echo "Téléchargement terminé."
