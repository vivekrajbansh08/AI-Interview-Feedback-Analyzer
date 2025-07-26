from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WeakAnswer(BaseModel):
    question: str
    original_answer: str
    issues: List[str]
    suggestions: List[str]
    improved_example: str

class FillerWordAnalysis(BaseModel):
    word: str
    count: int
    timestamps: List[float]

class ConfidenceMarker(BaseModel):
    marker_type: str  # "hedge", "upspeak", "filler", etc.
    examples: List[str]
    impact: str
    suggestion: str

class FeedbackReport(BaseModel):
    interview_id: str
    transcript: str
    overall_score: float
    weak_answers: List[WeakAnswer]
    filler_words: List[FillerWordAnalysis]
    confidence_markers: List[ConfidenceMarker]
    jargon_usage: List[str]
    recommendations: List[str]
    created_at: datetime = datetime.now()

class UploadResponse(BaseModel):
    success: bool
    message: str
    interview_id: Optional[str] = None
    transcript: Optional[str] = None
