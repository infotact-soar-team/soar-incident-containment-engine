from app.core.celery_app import celery_app
from uuid import UUID
from app.core.logging_config import logger
from app.database.session import SessionLocal
from app.models.ioc import IOC
from app.integrations.abuseipdb import check_ip
from app.integrations.geoip import lookup_ip_location
from app.integrations.virustotal import check_hash, check_domain
from app.services.risk_aggregator import aggregate_risk
from app.services.rule_engine import evaluate_alert
from app.services.incident_service import create_incident, log_actions
from app.playbooks.loader import load_playbook
from app.playbooks.engine import PlaybookEngine
from app.services.alert_lifecycle import transition_alert  # ✅ ensure lifecycle transitions are imported

# ✅ Mapping between playbook names and their file paths
PLAYBOOK_FILE_MAP = {
    "malicious_ip_playbook": "app/playbooks/malicious_ip_playbook.yml",
    "suspicious_ip_playbook": "app/playbooks/suspicious_ip_playbook.yml",
    "malicious_domain_playbook": "app/playbooks/malicious_domain_playbook.yml",
    "malware_hash_playbook": "app/playbooks/malware_hash_playbook.yml",
}

AUTO_CONTAIN_PLAYBOOKS = {
    "ip": "malicious_ip_playbook",
    "domain": "malicious_domain_playbook",
    "hash": "malware_hash_playbook",
}


@celery_app.task(name="enrich_ioc_task")
def enrich_ioc_task(ioc_id: str, ioc_type: str, ioc_value: str):
    """
    Full enrichment pipeline for a single IoC.
    Persists risk_score, severity, and recommended_action back to the IOC row.
    """
    db = SessionLocal()
    try:
        if ioc_type == "ip":
            abuseipdb_result = check_ip(ioc_value)
            lookup_ip_location(ioc_value)  # fetched for geo-based rules
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

        try:
            persisted_ioc_id = UUID(ioc_id)
        except (TypeError, ValueError, AttributeError):
            # Enrichment can also be invoked for an indicator that has not yet
            # been persisted (for example, a dry run or direct task call).
            ioc = None
        else:
            ioc = db.query(IOC).filter(IOC.id == persisted_ioc_id).first()
        incident_id = None
        if ioc:
            ioc.risk_score = risk_score
            ioc.severity = evaluation["severity"]
            ioc.recommended_action = evaluation["recommended_action"]
            db.commit()

            try:
                transition_alert(str(ioc.alert_id), "enriched")
            except Exception as e:
                logger.info(f"Lifecycle transition skipped: {e}")

            if evaluation["recommended_action"] == "AUTO_CONTAIN":
                playbook_name = AUTO_CONTAIN_PLAYBOOKS.get(ioc_type)
                if playbook_name:
                    incident_id = create_incident(
                        str(ioc.alert_id), str(ioc.id), playbook_name
                    )
                    playbook = load_playbook(PLAYBOOK_FILE_MAP[playbook_name])
                    action_results = PlaybookEngine(playbook).execute(ioc_value)
                    log_actions(incident_id, action_results)

        logger.info(f"Enriched {ioc_type}={ioc_value}: risk_score={risk_score}, severity={evaluation['severity']}")

        return {
            "ioc_id": ioc_id,
            "status": "enriched",
            "risk_score": risk_score,
            "severity": evaluation["severity"],
            "recommended_action": evaluation["recommended_action"],
            "incident_id": incident_id,
        }

    except Exception as e:
        logger.error(f"Enrichment failed for {ioc_type}={ioc_value}: {e}")
        return {"ioc_id": ioc_id, "status": "error", "error": str(e)}
    finally:
        db.close()
