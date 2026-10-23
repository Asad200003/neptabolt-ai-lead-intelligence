import io
import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import Company, LeadSource, DiscoveryJob
from app.services.normalization import normalize_domain, check_for_duplicates

def run_demo_mock_connector(job_id: str, db: Session):
    """Mock Lead Discovery with Normalization & Deduplication Checks"""
    mock_leads = [
        {
            "name": "Acme Tech Solutions Inc.",
            "domain": "https://www.acmetech.com/about",
            "industry": "Software & Cloud Services",
            "location": "San Francisco, CA",
            "company_size": "50-200 employees",
            "website_url": "https://acmetech.com"
        },
        {
            "name": "Global Logistics Corp",
            "domain": "globallogistics.io",
            "industry": "Supply Chain & Freight",
            "location": "New York, NY",
            "company_size": "500-1000 employees",
            "website_url": "https://globallogistics.io"
        },
        {
            "name": "BioHealth Innovations LLC",
            "domain": "http://biohealth.org",
            "industry": "Healthcare & Biotech",
            "location": "Boston, MA",
            "company_size": "10-50 employees",
            "website_url": "https://biohealth.org"
        }
    ]

    job = db.query(DiscoveryJob).filter(DiscoveryJob.id == job_id).first()
    if not job:
        return

    job.status = "RUNNING"
    db.commit()

    saved_count = 0
    for lead in mock_leads:
        norm_domain = normalize_domain(lead["domain"])
        dup_check = check_for_duplicates(norm_domain, lead["name"], db)
        
        review_status = "NEW"
        if dup_check["is_duplicate"]:
            review_status = "NEEDS_REVIEW" if dup_check["match_type"] == "NAME_MATCH_NEEDS_REVIEW" else "DUPLICATE"

        company = Company(
            discovery_job_id=job_id,
            name=lead["name"],
            domain=norm_domain,
            industry=lead["industry"],
            location=lead["location"],
            company_size=lead["company_size"],
            website_url=lead["website_url"],
            review_status=review_status
        )
        db.add(company)
        db.flush()

        source = LeadSource(
            company_id=company.id,
            source_name="DEMO_MOCK",
            source_url=lead["website_url"],
            raw_data=lead
        )
        db.add(source)
        saved_count += 1

    job.status = "COMPLETED"
    job.leads_found = saved_count
    db.commit()


def process_csv_import(file_bytes: bytes, db: Session):
    """CSV Import with Normalization Integration"""
    df = pd.read_csv(io.BytesIO(file_bytes))
    
    saved_count = 0
    for _, row in df.iterrows():
        name = str(row.get("name", row.get("Company Name", "Unknown Company")))
        raw_domain = str(row.get("domain", row.get("Domain", "")))
        norm_domain = normalize_domain(raw_domain)
        industry = str(row.get("industry", row.get("Industry", "")))
        location = str(row.get("location", row.get("Location", "")))
        
        company = Company(
            name=name,
            domain=norm_domain if norm_domain else None,
            industry=industry if industry else None,
            location=location if location else None,
            review_status="NEW"
        )
        db.add(company)
        db.flush()

        source = LeadSource(
            company_id=company.id,
            source_name="CSV_IMPORT",
            raw_data=row.to_dict()
        )
        db.add(source)
        saved_count += 1

    db.commit()
    return saved_count