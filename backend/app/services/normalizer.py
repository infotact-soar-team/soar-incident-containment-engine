from datetime import datetime
from app.schemas.alert import NormalizedAlert

SEVERITY_MAP = {
    "critical": "high",
    "high": "high",
    "warning": "medium",
    "medium": "medium",
    "info": "low",
    "low": "low",
}


def normalize_alert(raw_payload: dict) -> NormalizedAlert:
    """
    Converts a raw SIEM alert (arbitrary JSON shape) into our internal
    normalized schema. Handles missing/inconsistent field names gracefully.
    """
    source = raw_payload.get("source", "unknown")

    raw_severity = str(raw_payload.get("severity", "info")).lower()
    severity = SEVERITY_MAP.get(raw_severity, "low")

    message = raw_payload.get("message") or raw_payload.get("description") or "No message provided"

    raw_ts = raw_payload.get("timestamp")
    if raw_ts:
        try:
            timestamp = datetime.fromisoformat(raw_ts)
        except (ValueError, TypeError):
            timestamp = datetime.utcnow()
    else:
        timestamp = datetime.utcnow()

    return NormalizedAlert(
        source=source,
        severity=severity,
        message=message,
        timestamp=timestamp,
        raw_source_field=raw_payload.get("source"),
    )