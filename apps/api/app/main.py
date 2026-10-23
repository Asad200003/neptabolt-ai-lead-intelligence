from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import icps, jobs, leads, connectors, enrichment

app = FastAPI(
    title="Neptabolt AI Lead Intelligence Platform API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(icps.router)
app.include_router(jobs.router)
app.include_router(leads.router)
app.include_router(connectors.router)
app.include_router(enrichment.router)

@app.get("/")
def root():
    return {"message": "Neptabolt AI Lead Intelligence Platform API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}