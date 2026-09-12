from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.models.enums import JobStatus
from app.models.responses import ResearchJobDetail

_jobs: Dict[str, ResearchJobDetail] = {}


def create_job(job_id: str, topic: str) -> ResearchJobDetail:
    now = datetime.now(timezone.utc)
    job = ResearchJobDetail(
        job_id=job_id,
        status=JobStatus.PENDING,
        topic=topic,
        created_at=now,
        updated_at=now,
    )
    _jobs[job_id] = job
    return job


def get_job(job_id: str) -> Optional[ResearchJobDetail]:
    return _jobs.get(job_id)


def list_jobs() -> List[ResearchJobDetail]:
    return sorted(_jobs.values(), key=lambda j: j.created_at, reverse=True)


def delete_job(job_id: str) -> bool:
    if job_id in _jobs:
        del _jobs[job_id]
        return True
    return False


def update_job(job_id: str, **fields) -> None:
    """Patch arbitrary fields on a job and bump updated_at."""
    job = _jobs.get(job_id)
    if job is None:
        return
    for key, value in fields.items():
        setattr(job, key, value)
    job.updated_at = datetime.now(timezone.utc)