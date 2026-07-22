from app.core.celery_app import celery_app
from app.core.logging_config import logger
from app.integrations.abuseipdb import check_ip
from app.integrations.geoip import lookup_ip_location
from app.integrations.virustotal import check_hash, check_domain
from app.services.risk_aggregator import aggregate_risk
from app.services.rule_engine import evaluate_alert


@celery_app.task(name="enrich_ioc_task")
def enrich_ioc_task(ioc_id: str, ioc_type: str, ioc_value: str):
    """
    Full enrichment pipeline for a single IoC:
    1. Call the right TI integration(s) based on ioc_type
    2. Aggregate the result into a single risk score
    3. Feed the risk score into the rule engine for severity + action
    """
    try:
        if ioc_type == "ip":
            abuseipdb_result = check_ip(ioc_value)
            geoip_result = lookup_ip_location(ioc_value)
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