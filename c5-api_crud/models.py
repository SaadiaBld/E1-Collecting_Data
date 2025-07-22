
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Review(BaseModel):
    review_id: str
    rating: int
    content: str
    author: str
    publication_date: datetime
    scrape_date: datetime


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReviewIn(BaseModel):
    review_id: str
    rating: int
    content: str
    author: str
    publication_date: datetime
    scrape_date: datetime
    
class ReviewUpdate(BaseModel):
    content: str

class TopicAnalysis(BaseModel):
    id: str
    review_id: str
    topic_id: str
    score_sentiment: float
    label_sentiment: str
    score_0_1: float

class Topic(BaseModel):
    topic_id: str
    topic_label: str
    description: str

class TopicAnalysisUpdate(BaseModel):
    score_sentiment: float
    label_sentiment: str
    score_0_1: float
