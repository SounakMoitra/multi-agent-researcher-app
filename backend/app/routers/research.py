import uuid
from typing import List
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.requests import ResearchRequest
from app.models.responses import ResearchJobDetail, ResearchJobResponse
from app.services import job_store
from app.services.orchestrator import run_research_job

router = APIRouter(prefix="/api/research", tags=["Research"])


@router.post("", response_model=ResearchJobResponse, status_code=202)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Start a new research job. Returns immediately with a job_id to poll."""
    job_id = str(uuid.uuid4())
    job = job_store.create_job(job_id, request.topic)

    background_tasks.add_task(run_research_job, job_id, request.topic, request.model_name)

    return ResearchJobResponse(
        job_id=job.job_id,
        status=job.status,
        topic=job.topic,
        created_at=job.created_at,
    )


@router.get("/{job_id}", response_model=ResearchJobDetail)
async def get_research_job(job_id: str):
    """Get the current status and results (partial or complete) of a research job."""
    job = job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("", response_model=List[ResearchJobResponse])
async def list_research_jobs():
    """List all research jobs (most recent first)."""
    return [
        ResearchJobResponse(
            job_id=j.job_id, status=j.status, topic=j.topic, created_at=j.created_at
        )
        for j in job_store.list_jobs()
    ]


@router.delete("/{job_id}")
async def delete_research_job(job_id: str):
    """Delete a research job from the store."""
    if not job_store.delete_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}