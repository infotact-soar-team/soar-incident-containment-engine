from app.core.logging_config import logger
from app.database.session import SessionLocal
from app.models.alert import Alert


def transition_alert(alert_id: str, new_status: str) -> None:
    """
    Update the lifecycle status of an alert.
    Called after enrichment or containment to reflect progress.
    """
    db = SessionLocal()
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            logger.warning(f"Alert {alert_id} not found for lifecycle transition.")
            return

        alert.status = new_status
        db.commit()
        logger.info(f"Alert {alert_id} transitioned to '{new_status}'.")
    except Exception as e:
        logger.error(f"Failed to transition alert {alert_id}: {e}")
    finally:
        db.close()

