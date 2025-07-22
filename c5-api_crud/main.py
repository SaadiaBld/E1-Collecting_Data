from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException
from typing import List
import bigquery_service
from models import Review, ReviewIn, ReviewUpdate, TopicAnalysis, TopicAnalysisUpdate, Topic
import json

app = FastAPI()

@app.get("/reviews", response_model=List[Review])
def read_reviews():
    return bigquery_service.get_reviews()

@app.get("/reviews/{review_id}")
def read_review(review_id: str):
    review = bigquery_service.get_review(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

def clean_date_fields(data: dict) -> dict:
    for field in ["publication_date", "scrape_date"]:
        if field in data and isinstance(data[field], str):
            data[field] = data[field].split("T")[0]  # garde uniquement YYYY-MM-DD
    return data

@app.post("/reviews", status_code=201)
def create_review(review: ReviewIn):
    print(f"--- DEBUG: Payload reçu ---\n{review.dict()}")
    try:
        payload = jsonable_encoder(review)  # convertit les datetime en iso string
        payload = clean_date_fields(payload)  # assure que les dates sont en format ISO
        print(f"--- Payload encodable ---\n{payload}")
        success = bigquery_service.create_review(payload)
        if not success:
            raise HTTPException(status_code=400, detail="Error creating review")
        return review
    except Exception as e:
        print(f"--- EXCEPTION in create_review ---\n{e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/reviews/{review_id}")
def update_review(review_id: str, review: ReviewUpdate):
    updated_review = bigquery_service.update_review(review_id, review.dict())
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@app.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    result = bigquery_service.delete_review(review_id)
    return result

@app.get("/topics", response_model=List[Topic])
def read_topics():
    return bigquery_service.get_topics()
