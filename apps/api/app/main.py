from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.db import models

from app.api.icps import router as icps_router
from app.api.jobs import router as jobs_router
from app.api.leads import router as leads_router
from app.api.connectors import router as connectors_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Neptabolt AI Lead Intelligence API",
    description="API for ICP Management, Discovery Jobs, Lead Scoring, and Enrichment",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers Register Kar Rahe Hain
app.include_router(icps_router)
app.include_router(jobs_router)
app.include_router(leads_router)
app.include_router(connectors_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok", 
        "service": "Neptabolt API is Running Successfully!",
        "database": "Tables Verified & Created!"
    }