from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Company, LeadEnrichment
from app.services.enrichment import enrich_lead_with_ai

router = APIRouter(prefix="/api/enrichments", tags=["AI Enrichments"])

@router.post("/{company_id}")
def trigger_lead_enrichment(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    enrichment_data = enrich_lead_with_ai(company.name, company.domain or "")

    enrichment_record = LeadEnrichment(
        company_id=company.id,
        enriched_data_json=enrichment_data,
        confidence_score=enrichment_data["confidence_score"]
    )
    db.add(enrichment_record)
    db.commit()
    db.refresh(enrichment_record)

    return {
        "message": "Lead enriched successfully",
        "enrichment_id": enrichment_record.id,
        "company_id": company.id,
        "confidence_score": enrichment_record.confidence_score,
        "details": enrichment_data
    }