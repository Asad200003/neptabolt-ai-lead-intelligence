from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.connectors import process_csv_import

router = APIRouter(prefix="/api/connectors", tags=["Connectors"])

@router.get("/")
def list_connectors():
    return [
        {"id": "DEMO_MOCK", "name": "Deterministic Demo Connector", "status": "ACTIVE", "type": "Mock"},
        {"id": "CSV_IMPORT", "name": "CSV File Import Connector", "status": "ACTIVE", "type": "File"}
    ]

@router.post("/import-csv")
async def import_csv_leads(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    contents = await file.read()
    count = process_csv_import(contents, db)
    return {"message": f"Successfully imported {count} leads from CSV"}