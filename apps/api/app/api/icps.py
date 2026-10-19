from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import ICPProfile
from app.schemas.schemas import ICPProfileCreate, ICPProfileResponse

router = APIRouter(prefix="/api/icps", tags=["ICP Profiles"])

@router.post("/", response_model=ICPProfileResponse)
def create_icp(icp: ICPProfileCreate, db: Session = Depends(get_db)):
    db_icp = ICPProfile(
        name=icp.name,
        description=icp.description,
        target_industry=icp.target_industry,
        target_location=icp.target_location,
        criteria_json=icp.criteria_json
    )
    db.add(db_icp)
    db.commit()
    db.refresh(db_icp)
    return db_icp

@router.get("/", response_model=List[ICPProfileResponse])
def list_icps(db: Session = Depends(get_db)):
    return db.query(ICPProfile).all()