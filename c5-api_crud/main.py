
from fastapi import FastAPI, HTTPException
from typing import List
import bigquery_service
from models import Review, ReviewIn, ReviewUpdate, TopicAnalysis, TopicAnalysisUpdate, Topic

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

@app.post("/reviews", status_code=201)
def create_review(review: ReviewIn):
    success = bigquery_service.create_review(review.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Error creating review")
    return review

@app.put("/reviews/{review_id}")
def update_review(review_id: str, review: ReviewUpdate):
    updated_review = bigquery_service.update_review(review_id, review.dict())
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@app.put("/analysis/{analysis_id}")
def update_topic_analysis(analysis_id: str, analysis: TopicAnalysisUpdate):
    updated_analysis = bigquery_service.update_topic_analysis(analysis_id, analysis.dict())
    if not updated_analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return updated_analysis

@app.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    result = bigquery_service.delete_review(review_id)
    return result

@app.get("/topics", response_model=List[Topic])
def read_topics():
    return bigquery_service.get_topics()
