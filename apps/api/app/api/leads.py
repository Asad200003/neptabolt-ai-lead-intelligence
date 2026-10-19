from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import Company
from app.schemas.schemas import CompanyResponse

router = APIRouter(prefix="/api/leads", tags=["Leads"])

@router.get("/", response_model=List[CompanyResponse])
def list_leads(db: Session = Depends(get_db)):
    return db.query(Company).all()