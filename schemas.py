from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class QuestionRequest(BaseModel):
    question: str
    session_id: str  # ties question to an uploaded log file


class QuestionResponse(BaseModel):
    question: str
    answer: str
    session_id: str


class ErrorEntry(BaseModel):
    line_number: Optional[int]
    error_type: str
    message: str
    severity: str  # CRITICAL, ERROR, WARNING


class IncidentReport(BaseModel):
    session_id: str
    filename: str
    generated_at: str
    total_lines_analyzed: int
    error_summary: str
    errors_found: List[ErrorEntry]
    root_cause_analysis: str
    recommended_actions: List[str]
    severity_level: str  # HIGH, MEDIUM, LOW


class UploadResponse(BaseModel):
    message: str
    session_id: str
    filename: str
    total_chunks: int
    hint: str
