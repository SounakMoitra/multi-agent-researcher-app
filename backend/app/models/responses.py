from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.enums import JobStatus


class ResearchQuestion(BaseModel):
    question: str
    answer: str


class ResearchJobResponse(BaseModel):
    """Lightweight response returned right after starting a job, and in list views."""

    job_id: str
    status: JobStatus
    topic: str
    created_at: datetime


class ResearchJobDetail(BaseModel):
    """Full job record, including partial/complete results. Used as the job store's record type."""

    job_id: str
    status: JobStatus
    topic: str
    created_at: datetime
    updated_at: datetime
    plan: Optional[List[str]] = None
    research_results: Optional[List[ResearchQuestion]] = None
    final_report: Optional[str] = None
    error: Optional[str] = None