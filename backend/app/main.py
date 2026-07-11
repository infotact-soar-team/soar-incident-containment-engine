from fastapi import FastAPI

app = FastAPI(
    title="SOAR Incident Containment Engine",
    version="0.1.0",
    description="Enterprise SOAR platform - webhook ingestion, enrichment, and automated containment"
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "soar-incident-engine"}


@app.get("/")
def root():
    return {"message": "SOAR Incident Containment Engine API is running"}