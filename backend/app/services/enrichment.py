from app.schemas.enrichment import EnrichmentResult

# NOTE: This is a skeleton for Day 4. Live API calls to AbuseIPDB,
# VirusTotal, and GeoIP are implemented in Week 2.


def enrich_ip(ip: str) -> EnrichmentResult:
    """
    Will call AbuseIPDB + GeoIP for a given IP in Week 2.
    For now, returns a placeholder result so other modules can
    integrate against the expected shape.
    """
    return EnrichmentResult(
        ioc_value=ip,
        ioc_type="ip",
        abuse_confidence_score=None,
        geo_country=None,
        risk_score=None,
    )


def enrich_hash(file_hash: str) -> EnrichmentResult:
    """
    Will call VirusTotal for a given file hash in Week 2.
    """
    return EnrichmentResult(
        ioc_value=file_hash,
        ioc_type="hash",
        vt_malicious_count=None,
        risk_score=None,
    )


def enrich_domain(domain: str) -> EnrichmentResult:
    """
    Will call VirusTotal for a given domain in Week 2.
    """
    return EnrichmentResult(
        ioc_value=domain,
        ioc_type="domain",
        vt_malicious_count=None,
        risk_score=None,
    )