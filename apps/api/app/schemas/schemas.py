from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- ICP SCHEMAS ---
class ICPProfileBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_industry: Optional[str] = None
    target_location: Optional[str] = None
    criteria_json: Optional[Dict[str, Any]] = None

class ICPProfileCreate(ICPProfileBase):
    pass

class ICPProfileResponse(ICPProfileBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- DISCOVERY JOB SCHEMAS ---
class DiscoveryJobCreate(BaseModel):
    icp_profile_id: str
    requested_sources: Optional[List[str]] = ["DEMO_MOCK", "CSV_IMPORT"]

class DiscoveryJobResponse(BaseModel):
    id: str
    icp_profile_id: str
    status: str
    leads_found: int
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- COMPANY / LEAD SCHEMAS ---
class CompanyResponse(BaseModel):
    id: str
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    company_size: Optional[str] = None
    website_url: Optional[str] = None
    review_status: str
    created_at: datetime

    class Config:
        from_attributes = True