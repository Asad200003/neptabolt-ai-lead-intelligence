from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import DiscoveryJob, ICPProfile
from app.schemas.schemas import DiscoveryJobCreate, DiscoveryJobResponse
from app.services.connectors import run_demo_mock_connector

router = APIRouter(prefix="/api/discovery-jobs", tags=["Discovery Jobs"])

@router.post("/", response_model=DiscoveryJobResponse)
def create_discovery_job(
    job_in: DiscoveryJobCreate, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    icp = db.query(ICPProfile).filter(ICPProfile.id == job_in.icp_profile_id).first()
    if not icp:
        raise HTTPException(status_code=404, detail="ICP Profile not found")

    job = DiscoveryJob(
        icp_profile_id=job_in.icp_profile_id,
        requested_sources=job_in.requested_sources,
        status="QUEUED"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Background job triggers mock connector
    background_tasks.add_task(run_demo_mock_connector, job.id, db)

    return job

@router.get("/{job_id}", response_model=DiscoveryJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(DiscoveryJob).filter(DiscoveryJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Discovery Job not found")
    return job