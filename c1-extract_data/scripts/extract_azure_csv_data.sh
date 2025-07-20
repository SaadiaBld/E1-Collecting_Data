#!/bin/bash
#automatiser le telechargelent de fichiers csv stockés dansun conteneur azure blob storage dans un dossier nlp_data vers un repertoire local
# Utilise azure CLI (az) pour generer les tokens  sas et les clés d'accès, azcopy pour le téléchargement des fichiers
# bash pour l'automatisation

# 1/ Configuration des variables du compte de stockage, du groupe de ressources du conteneur,..
STORAGE_ACCOUNT="datalakedeviavals"   # Nom du compte de stockage
CONTAINER_NAME="data"                # Nom du conteneur
RESOURCE_GROUP="RG_VANGANSBERGJ"     # Nom du groupe de ressources
LOCAL_DIR="./data/extraction_from_blobs"               # Répertoire local pour les téléchargements
EXPIRY_TIME=$(date -u -d "+24 hours" +"%Y-%m-%dT%H:%M:%SZ") # Expiration dans 24h

# 2/ Créer le répertoire local si n'existe pas 
mkdir -p "$LOCAL_DIR"

# 3/ Vérifie si AzCopy est installé
if ! command -v azcopy &> /dev/null; then
    echo "Erreur : AzCopy n'est pas installé. Installez-le avant d'exécuter ce script."
    exit 1
fi

# 4/ Récupération de la clé d'accès du compte de stockage avec azure CLI
echo "Récupération de la clé d'accès pour le compte de stockage..."
ACCOUNT_KEY=$(az storage account keys list --resource-group "$RESOURCE_GROUP" --account-name "$STORAGE_ACCOUNT" --query "[0].value" --output tsv)

# 5/ Vérification si ACCOUNT_KEY a été récupéré 
if [ -z "$ACCOUNT_KEY" ]; then
    echo "Erreur : Impossible de récupérer la clé d'accès pour le compte de stockage."
    exit 1
fi

# 6/ Récupération des blobs CSV et filtrage des blobs qui commencent par 'nlp_data/' et se terminent par '.csv'
echo "Récupération des blobs dans le conteneur Azure..."
BLOBS=$(az storage blob list --account-name "$STORAGE_ACCOUNT" --account-key "$ACCOUNT_KEY" --container-name "$CONTAINER_NAME" \
     --query "[?starts_with(name, 'nlp_data/') && ends_with(name, '.csv')].name" --output tsv)


# 8/ Vérification si des blobs existent
if [ -z "$BLOBS" ]; then
    echo "Aucun blob trouvé dans le conteneur $CONTAINER_NAME."
    exit 0
fi

# 9/ Génération d'un SAS Token: creer un lien d'accès temporaire pour accéder aux blobs
echo "Génération d'un SAS Token pour un accès temporaire..."
SAS_TOKEN=$(az storage container generate-sas \
    --account-name "$STORAGE_ACCOUNT" \
    --name "$CONTAINER_NAME" \
    --permissions rl \
    --expiry "$EXPIRY_TIME" \
    --output tsv)

# 10/ fonction url-safe pour encoder les caractères spéciaux dans les noms de blobs et les rendre sûrs
urlencode() {
    local STRING="$1"
    local ENCODED=""
    local i
    for (( i=0; i<${#STRING}; i++ )); do
        local CHAR="${STRING:$i:1}"
        case "$CHAR" in
            [a-zA-Z0-9.~_,-]) ENCODED+="$CHAR" ;;  # Inclure l'apostrophe et la virgule
            *) ENCODED+=$(printf '%%%02X' "'$CHAR") ;;  # Encodage des autres caractères
        esac
    done
    echo "$ENCODED"
}

# 11/ Fonction pour télécharger un blob spécifique 
download_blob() {
    local BLOB="$1"
    
    # Encodage du nom du blob pour l'URL
    local ENCODED_BLOB=$(urlencode "$BLOB")
    
    # Suppression du préfixe `nlp_data/` dans le chemin local
    local LOCAL_PATH="$LOCAL_DIR/$(echo "$BLOB" | sed 's/^nlp_data\///')"
    
    # Création des répertoires locaux nécessaires
    mkdir -p "$(dirname "$LOCAL_PATH")"
    
    # Génération de l'URL complète pour le blob
    local SAS_URL="https://$STORAGE_ACCOUNT.blob.core.windows.net/$CONTAINER_NAME/$BLOB_NAME?$SAS_TOKEN"
    echo "Téléchargement de : $BLOB"
    azcopy copy "$SAS_URL" "$LOCAL_PATH" --recursive --overwrite=true
    
    # Vérification du succès du téléchargement
    if [ $? -ne 0 ]; then
        echo "Erreur lors du téléchargement de $BLOB. Le script continue avec les autres fichiers."
    else
        echo "Téléchargement réussi : $BLOB téléchargé dans $LOCAL_PATH"
    fi
}


# 12/ Téléchargement de tous les fichiers CSV
echo "Téléchargement des fichiers CSV..."
while IFS= read -r BLOB; do
    # Vérifie si le fichier est un .csv
    if [[ ! "$BLOB" =~ \.csv$ ]]; then
        #echo " Ignoré : $BLOB n'est pas un fichier CSV."
        #echo "⏭️ Ignoré : $BLOB (non .csv)"
        continue
    fi
    download_blob "$BLOB"
done <<< "$BLOBS"

echo "Téléchargement terminé. Tous les fichiers CSV valides ont été enregistrés dans $LOCAL_DIR."
