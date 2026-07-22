from app.core.celery_app import celery_app
from app.core.logging_config import logger
from app.database.session import SessionLocal
from app.models.ioc import IOC
from app.integrations.abuseipdb import check_ip
from app.integrations.geoip import lookup_ip_location
from app.integrations.virustotal import check_hash, check_domain
from app.services.risk_aggregator import aggregate_risk
from app.services.rule_engine import evaluate_alert


@celery_app.task(name="enrich_ioc_task")
def enrich_ioc_task(ioc_id: str, ioc_type: str, ioc_value: str):
    """
    Full enrichment pipeline for a single IoC. Now persists the result
    (risk_score, severity, recommended_action) back onto the IOC row,
    fixing the earlier mismatch where results were only logged/returned
    but never actually saved.
    """
    db = SessionLocal()
    try:
        if ioc_type == "ip":
            abuseipdb_result = check_ip(ioc_value)
            lookup_ip_location(ioc_value)  # fetched for future geo-based rules
            risk_score = aggregate_risk("ip", abuseipdb_result=abuseipdb_result)
        elif ioc_type == "hash":
            vt_result = check_hash(ioc_value)
            risk_score = aggregate_risk("hash", vt_result=vt_result)
        elif ioc_type == "domain":
            vt_result = check_domain(ioc_value)
            risk_score = aggregate_risk("domain", vt_result=vt_result)
        else:
            logger.info(f"Unknown IoC type '{ioc_type}' for {ioc_value}, skipping enrichment")
            return {"ioc_id": ioc_id, "status": "skipped", "reason": "unknown ioc_type"}

        evaluation = evaluate_alert(risk_score, ioc_value, ioc_type)

        ioc = db.query(IOC).filter(IOC.id == ioc_id).first()
        if ioc:
            ioc.risk_score = risk_score
            ioc.severity = evaluation["severity"]
            ioc.recommended_action = evaluation["recommended_action"]
            db.commit()

        logger.info(f"Enriched {ioc_type}={ioc_value}: risk_score={risk_score}, severity={evaluation['severity']}")

        return {
            "ioc_id": ioc_id,
            "status": "enriched",
            "risk_score": risk_score,
            "severity": evaluation["severity"],
            "recommended_action": evaluation["recommended_action"],
        }

    except Exception as e:
        logger.error(f"Enrichment failed for {ioc_type}={ioc_value}: {e}")
        return {"ioc_id": ioc_id, "status": "error", "error": str(e)}
    finally:
        db.close()