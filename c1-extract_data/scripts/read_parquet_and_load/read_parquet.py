import os
import pandas as pd
from PIL import Image
import io, sys


parquet_files_dir = 'data/extraction_from_parquet'
images_dir = os.path.join(parquet_files_dir, "images")
metadata_dir = os.path.join(parquet_files_dir, "metadata")

# Vérification du dossier parquet source
if not os.path.isdir(parquet_files_dir):
    print(f"❌ Dossier introuvable : {parquet_files_dir}")
    sys.exit(1)

# Créer les dossiers de sortie principaux
os.makedirs(images_dir, exist_ok=True)
os.makedirs(metadata_dir, exist_ok=True)

# Lister les fichiers .parquet
parquet_files = [file for file in os.listdir(parquet_files_dir) if file.endswith('.parquet')]

if not parquet_files:
    print(f"Aucun fichier Parquet trouvé dans {parquet_files_dir}")
    sys.exit(1)

image_format = 'png'  # Ou 'jpeg'

for parquet_file_name in parquet_files:
    subfolder_name, _, _ = parquet_file_name.partition('.')
    subfolder_path = os.path.join(images_dir, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)

    df = pd.read_parquet(os.path.join(parquet_files_dir, parquet_file_name))

    image_paths = []

    for idx, row in df.iterrows():
        try:
            image_bytes = row['image']['bytes']
            item_id = row['item_ID']

            image = Image.open(io.BytesIO(image_bytes))

            if image.mode == 'RGBA' and image_format == 'jpeg':
                image = image.convert('RGB')

            image_path = os.path.join(subfolder_path, f"{item_id}.{image_format}")
            image.save(image_path, format=image_format.upper())

            image_paths.append(image_path)
        except Exception as e:
            print(f"Erreur lors du traitement de l'image index {idx} dans {parquet_file_name}: {e}")
            image_paths.append("")
            
    df['image_path'] = image_paths

    metadata_filename = os.path.join(metadata_dir, f"metadata_{subfolder_name}.csv")
    df[['item_ID', 'query', 'title', 'position', 'image_path']].to_csv(metadata_filename, index=False)

    print(f"✅ Fichier traité : {parquet_file_name}")
    print(f"→ Images dans : {subfolder_path}")
    print(f"→ Métadonnées dans : {metadata_filename}\n")
