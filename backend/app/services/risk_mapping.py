"""
Risk score (0-100) to severity + recommended action mapping.
Bands are now loaded from an editable YAML config instead of being hardcoded,
so thresholds can be tuned without touching code.
"""
import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "severity_thresholds.yaml")


def _load_bands() -> list:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config["bands"]


RISK_BANDS = _load_bands()


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
