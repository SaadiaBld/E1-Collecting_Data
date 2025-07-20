#!/bin/bash

# Variables nécessaires
STORAGE_ACCOUNT="datalakedeviavals"
CONTAINER_NAME="data"
BLOB_NAMES=("machine_learning/reviews.zip")
PERMISSIONS="r"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EXPIRY_TIME=$(date -u -d "+24 hours" +"%Y-%m-%dT%H:%M:%SZ")
RESOURCE_GROUP="RG_VANGANSBERGJ"

# Dossier cible
DEST_DIR="data/extraction_zip_files"
mkdir -p "$DEST_DIR"

# Récupérer la clé du compte de stockage
ACCOUNT_KEY=$(az storage account keys list \
    --resource-group $RESOURCE_GROUP \
    --account-name $STORAGE_ACCOUNT \
    --query "[0].value" --output tsv)

if [ -z "$ACCOUNT_KEY" ]; then
    echo " Erreur : clé d'accès non récupérée."
    exit 1
fi

for BLOB_NAME in "${BLOB_NAMES[@]}"; do
    SAS_TOKEN=$(az storage blob generate-sas \
        --account-name $STORAGE_ACCOUNT \
        --account-key $ACCOUNT_KEY \
        --container-name $CONTAINER_NAME \
        --name $BLOB_NAME \
        --permissions $PERMISSIONS \
        --start $START_TIME \
        --expiry $EXPIRY_TIME \
        --https-only \
        --output tsv)

    if [ -z "$SAS_TOKEN" ]; then
        echo " Erreur : SAS token non généré pour $BLOB_NAME."
        exit 1
    fi

    FILE_NAME=$(basename "$BLOB_NAME")
    SAS_URL="https://$STORAGE_ACCOUNT.blob.core.windows.net/$CONTAINER_NAME/$BLOB_NAME?$SAS_TOKEN"

    echo "Téléchargement de $FILE_NAME..."
    wget "$SAS_URL" -O "$DEST_DIR/$FILE_NAME"
    if [ $? -ne 0 ]; then
        echo "Erreur lors du téléchargement de $FILE_NAME"
        continue
    fi

    echo "Décompression de $FILE_NAME..."
    unzip "$DEST_DIR/$FILE_NAME" -d "$DEST_DIR/"
    rm "$DEST_DIR/$FILE_NAME"

    # Extraire les éventuels .tgz
    for TGZ_FILE in "$DEST_DIR"/*.tgz; do
        [ -f "$TGZ_FILE" ] && tar -xzvf "$TGZ_FILE" -C "$DEST_DIR" && rm "$TGZ_FILE"
    done
done

echo "Tous les fichiers ont été extraits dans $DEST_DIR"
# Fin du script
