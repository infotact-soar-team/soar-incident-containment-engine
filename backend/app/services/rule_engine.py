"""
Rule Engine Prototype — decides what action to take based on a risk score.
Currently accepts a manually-computed risk score (dummy data).
Once enrichment aggregation (risk_aggregator) is ready later this week,
this will receive its input from there automatically.
"""
from app.services.risk_mapping import severity_for_score, action_for_score


def evaluate_alert(risk_score: int, ioc_value: str, ioc_type: str) -> dict:
    """
    Given a risk score for an IoC, determine severity and recommended action.
    This is the entry point the playbook engine (Week 3) will call.
    """
    severity = severity_for_score(risk_score)
    action = action_for_score(risk_score)

    return {
        "ioc_value": ioc_value,
        "ioc_type": ioc_type,
        "risk_score": risk_score,
        "severity": severity,
        "recommended_action": action,
    }
