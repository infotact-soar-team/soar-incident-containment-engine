"""
Combines signals from AbuseIPDB, VirusTotal, and GeoIP into a single
0-100 risk score, which the rule engine then maps to a severity/action.
"""

def aggregate_ip_risk(abuseipdb_result: dict, geoip_result: dict = None) -> int:
    """
    Risk score for an IP based on AbuseIPDB confidence score,
    with GeoIP as supplementary context (not currently score-affecting,
    reserved for future geo-based rules).
    """
    score = abuseipdb_result.get("abuse_confidence_score") or 0
    return min(max(score, 0), 100)


def aggregate_hash_or_domain_risk(vt_result: dict) -> int:
    """
    Risk score for a hash/domain based on VirusTotal detection ratio.
    Converts malicious/suspicious detections into a 0-100 score.
    """
    malicious = vt_result.get("malicious", 0)
    suspicious = vt_result.get("suspicious", 0)
    harmless = vt_result.get("harmless", 0)
    undetected = vt_result.get("undetected", 0)

    total_engines = malicious + suspicious + harmless + undetected
    if total_engines == 0:
        return 0

    weighted = (malicious * 1.0) + (suspicious * 0.5)
    score = int((weighted / total_engines) * 100)
    return min(max(score, 0), 100)


def aggregate_risk(ioc_type: str, **enrichment_data) -> int:
    """
    Single entry point: dispatch to the right aggregator based on ioc_type.
    """
    if ioc_type == "ip":
        return aggregate_ip_risk(
            enrichment_data.get("abuseipdb_result", {}),
            enrichment_data.get("geoip_result"),
        )
    elif ioc_type in ("hash", "domain"):
        return aggregate_hash_or_domain_risk(enrichment_data.get("vt_result", {}))
    return 0
