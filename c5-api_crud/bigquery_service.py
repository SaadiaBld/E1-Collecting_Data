import os
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
from pathlib import Path

# --- Chargement du fichier .env ---
dotenv_path = Path(__file__).resolve().parent / "config" / ".env"
if not dotenv_path.exists():
    raise FileNotFoundError(f"Le fichier .env est introuvable : {dotenv_path}")
load_dotenv(dotenv_path)

# --- Variables d'environnement ---
PROJECT_ID = os.getenv("PROJECT_ID")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not PROJECT_ID:
    raise ValueError("PROJECT_ID est manquant dans le .env")
if not GOOGLE_CREDENTIALS:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS est manquant dans le .env")

# --- Résolution absolue du fichier de credentials ---
GOOGLE_CREDENTIALS_ABS = os.path.abspath(
    os.path.join(os.path.dirname(__file__), GOOGLE_CREDENTIALS)
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_ABS
print(f"--- DEBUG: Clé GCP utilisée => {GOOGLE_CREDENTIALS_ABS}")

# --- Initialisation du client BigQuery ---
credentials = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS_ABS)
client = bigquery.Client(credentials=credentials)

# --- Constantes ---
DATASET_ID = "reviews_dataset"
REVIEWS_TABLE_ID = "reviews"
TOPIC_ANALYSIS_TABLE_ID = "topic_analysis"
TOPICS_TABLE_ID = "topics"

# --- Fonctions CRUD ---
def get_reviews():
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}`"
    return [dict(row) for row in client.query(query).result()]

def get_review(review_id: str):
    query = f"""
    SELECT r.*, ta.*
    FROM `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}` r
    LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.{TOPIC_ANALYSIS_TABLE_ID}` ta ON r.review_id = ta.review_id
    WHERE r.review_id = @review_id
    limit 10
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("review_id", "STRING", review_id)
        ]
    )
    return [dict(row) for row in client.query(query, job_config=job_config).result()]

def create_review(review: dict):
    for key, value in review.items():
        if isinstance(value, datetime):
            review[key] = value.isoformat()  # conversion explicite

    try:
        table = client.get_table(client.dataset(DATASET_ID).table(REVIEWS_TABLE_ID))
        errors = client.insert_rows_json(table, [review])

        if errors:
            print(f"--- DEBUG INSERT ERRORS ---\n{errors}")
            return False
        return True
    except Exception as e:
        print(f"--- EXCEPTION in create_review ---\n{e}")
        return False

def update_review(review_id: str, review_data: dict):
    query = f"""
    UPDATE `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}`
    SET content = @content
    WHERE review_id = @review_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("content", "STRING", review_data.get("content")),
            bigquery.ScalarQueryParameter("review_id", "STRING", review_id),
        ]
    )
    client.query(query, job_config=job_config).result()
    return get_review(review_id)

def update_topic_analysis(analysis_id: str, analysis_data: dict):
    query = f"""
    UPDATE `{PROJECT_ID}.{DATASET_ID}.{TOPIC_ANALYSIS_TABLE_ID}`
    SET
        score_sentiment = @score_sentiment,
        label_sentiment = @label_sentiment,
        score_0_1 = @score_0_1
    WHERE id = @analysis_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("score_sentiment", "FLOAT", analysis_data.get("score_sentiment")),
            bigquery.ScalarQueryParameter("label_sentiment", "STRING", analysis_data.get("label_sentiment")),
            bigquery.ScalarQueryParameter("score_0_1", "FLOAT", analysis_data.get("score_0_1")),
            bigquery.ScalarQueryParameter("analysis_id", "STRING", analysis_id),
        ]
    )
    client.query(query, job_config=job_config).result()
    return {"status": "success"}

def delete_review(review_id: str):
    client.query(f"DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{TOPIC_ANALYSIS_TABLE_ID}` WHERE review_id = '{review_id}'").result()
    client.query(f"DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}` WHERE review_id = '{review_id}'").result()
    return {"status": "success"}

def get_topics():
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TOPICS_TABLE_ID}`"
    return [dict(row) for row in client.query(query).result()]
