
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
print(f"--- DEBUG: PROJECT_ID lu depuis l'environnement : '{PROJECT_ID}' ---")
if not PROJECT_ID:
    raise ValueError("La variable d'environnement PROJECT_ID n'est pas définie. Veuillez la configurer dans votre fichier .env")

DATASET_ID = "reviews_dataset"
REVIEWS_TABLE_ID = "reviews"
TOPIC_ANALYSIS_TABLE_ID = "topic_analysis"
TOPICS_TABLE_ID = "topics"

client = bigquery.Client(project=PROJECT_ID)

def get_reviews():
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}`
    """
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]

def get_review(review_id: str):
    query = f"""
    SELECT r.*, ta.*
    FROM `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}` r
    LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.{TOPIC_ANALYSIS_TABLE_ID}` ta ON r.review_id = ta.review_id
    WHERE r.review_id = @review_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("review_id", "STRING", review_id),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    return [dict(row) for row in results]

def create_review(review: dict):
    table_ref = client.dataset(DATASET_ID).table(REVIEWS_TABLE_ID)
    table = client.get_table(table_ref)
    errors = client.insert_rows_json(table, [review])
    return errors == []

def update_review(review_id: str, review_data: dict):
    # Note: BigQuery is not ideal for record-level updates.
    # This is a simplified example. For production, consider a different approach.
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
    # BQ doesn't easily return the updated row, so we'll just return success
    return {"status": "success"}


def delete_review(review_id: str):
    # Note: This will delete the review and its corresponding analysis
    # using two separate delete statements.
    client.query(f"DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{TOPIC_ANALYSIS_TABLE_ID}` WHERE review_id = '{review_id}'").result()
    client.query(f"DELETE FROM `{PROJECT_ID}.{DATASET_ID}.{REVIEWS_TABLE_ID}` WHERE review_id = '{review_id}'").result()
    return {"status": "success"}

def get_topics():
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.{TOPICS_TABLE_ID}`
    """
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]
