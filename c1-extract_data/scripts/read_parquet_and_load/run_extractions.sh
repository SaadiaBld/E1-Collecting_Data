#!/bin/bash

echo " **** Génération des URLs SAS..."
bash scripts/read_parquet_and_load/generate_sas_parquet_urls.sh

echo " **** Téléchargement des fichiers .parquet..."
bash scripts/read_parquet_and_load/download_parquet_files.sh

echo " **** Extraction des images et métadonnées..."
python3 scripts/read_parquet_and_load/read_parquet.py
