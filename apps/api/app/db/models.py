import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class ICPProfile(Base):
    __tablename__ = "icp_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_industry = Column(String(255), nullable=True)
    target_location = Column(String(255), nullable=True)
    criteria_json = Column(JSON, nullable=True)  # Store detailed criteria & exclusions
    created_at = Column(DateTime, default=datetime.utcnow)

    discovery_jobs = relationship("DiscoveryJob", back_populates="icp_profile")


class DiscoveryJob(Base):
    __tablename__ = "discovery_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    icp_profile_id = Column(String, ForeignKey("icp_profiles.id"), nullable=False)
    status = Column(String(50), default="QUEUED")  # QUEUED, RUNNING, COMPLETED, FAILED
    requested_sources = Column(JSON, nullable=True)
    leads_found = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    icp_profile = relationship("ICPProfile", back_populates="discovery_jobs")
    companies = relationship("Company", back_populates="discovery_job")


class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    discovery_job_id = Column(String, ForeignKey("discovery_jobs.id"), nullable=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=True, index=True)
    industry = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    company_size = Column(String(100), nullable=True)
    website_url = Column(String(500), nullable=True)
    review_status = Column(String(50), default="NEW")  # NEW, RELEVANT, IRRELEVANT, NEEDS_REVIEW
    created_at = Column(DateTime, default=datetime.utcnow)

    discovery_job = relationship("DiscoveryJob", back_populates="companies")
    sources = relationship("LeadSource", back_populates="company")
    scores = relationship("LeadScore", back_populates="company")
    enrichments = relationship("Enrichment", back_populates="company")


class LeadSource(Base):
    __tablename__ = "lead_sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    source_name = Column(String(100), nullable=False)  # e.g., CSV_IMPORT, DEMO_MOCK
    source_url = Column(String(500), nullable=True)
    raw_data = Column(JSON, nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="sources")


class LeadScore(Base):
    __tablename__ = "lead_scores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    total_score = Column(Float, nullable=False)
    breakdown_json = Column(JSON, nullable=True)  # Criterion breakdown
    rationale = Column(Text, nullable=True)       # Human-readable explanation
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="scores")


class Enrichment(Base):
    __tablename__ = "enrichments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    field_name = Column(String(100), nullable=False)
    field_value = Column(Text, nullable=True)
    evidence = Column(Text, nullable=True)        # Source citation / text excerpt
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="enrichments")