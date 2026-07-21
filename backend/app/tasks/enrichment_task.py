from app.core.celery_app import celery_app
from app.core.logging_config import logger


@celery_app.task(name="enrich_ioc_task")
def enrich_ioc_task(ioc_id: str, ioc_type: str, ioc_value: str):
    """
    Async task that will call the real enrichment pipeline for a given IoC.
    For now, just logs the dispatch — actual enrichment wiring (calling
    abuseipdb/virustotal/geoip based on ioc_type) is completed once all
    3 live integrations are ready.
    """
    logger.info(f"Enrichment task dispatched: {ioc_type}={ioc_value} (ioc_id={ioc_id})")
    return {"ioc_id": ioc_id, "ioc_type": ioc_type, "ioc_value": ioc_value, "status": "dispatched"}