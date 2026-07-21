"""
Risk score (0-100) to severity + recommended action mapping.
This is the central reference used by the rule engine (Week 3)
to decide what containment action a given risk score should trigger.
"""

RISK_BANDS = [
    {"min": 71, "max": 100, "severity": "high", "action": "AUTO_CONTAIN"},
    {"min": 31, "max": 70, "severity": "medium", "action": "NOTIFY_ANALYST"},
    {"min": 0, "max": 30, "severity": "low", "action": "LOG_ONLY"},
]


def severity_for_score(risk_score: int) -> str:
    for band in RISK_BANDS:
        if band["min"] <= risk_score <= band["max"]:
            return band["severity"]
    return "low"


def action_for_score(risk_score: int) -> str:
    for band in RISK_BANDS:
        if band["min"] <= risk_score <= band["max"]:
            return band["action"]
    return "LOG_ONLY"

