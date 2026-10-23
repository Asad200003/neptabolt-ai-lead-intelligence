import re
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from app.db.models import Company

def normalize_domain(url_or_domain: str) -> str:
    """URLs aur domain strings se clean domain extract karta hai"""
    if not url_or_domain:
        return ""
    
    clean_str = url_or_domain.strip().lower()
    if not clean_str.startswith(("http://", "https://")):
        clean_str = "http://" + clean_str
        
    try:
        parsed = urlparse(clean_str)
        domain = parsed.netloc or parsed.path
        if domain.startswith("www."):
            domain = domain[4:]
        return domain.split(":")[0]  # Port number removing
    except Exception:
        return url_or_domain.strip().lower()


def normalize_company_name(name: str) -> str:
    """Legal suffixes clean karta hai (e.g., Acme Inc -> acme)"""
    if not name:
        return ""
    
    clean_name = name.strip()
    patterns = r"\b(inc|inc\.|llc|ltd|ltd\.|corp|corporation|gmbh|pvt|private|limited)\b"
    clean_name = re.sub(patterns, "", clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r"[^\w\s]", "", clean_name)
    return " ".join(clean_name.split()).lower()


def check_for_duplicates(domain: str, name: str, db: Session):
    """
    Conservative Duplicate Detection Logic:
    1. Exact Domain Match -> High Confidence Duplicate
    2. Normalized Name Match -> Flagged for Manual Review
    """
    clean_dom = normalize_domain(domain)
    clean_nm = normalize_company_name(name)

    # 1. Exact domain match check
    if clean_dom:
        domain_match = db.query(Company).filter(Company.domain == clean_dom).first()
        if domain_match:
            return {"is_duplicate": True, "match_type": "EXACT_DOMAIN", "company_id": domain_match.id}

    # 2. Name match check
    if clean_nm:
        all_companies = db.query(Company).all()
        for comp in all_companies:
            if normalize_company_name(comp.name) == clean_nm:
                return {"is_duplicate": True, "match_type": "NAME_MATCH_NEEDS_REVIEW", "company_id": comp.id}

    return {"is_duplicate": False, "match_type": None, "company_id": None}