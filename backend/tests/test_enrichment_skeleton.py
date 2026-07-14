from app.services.enrichment import enrich_ip, enrich_hash, enrich_domain


def test_enrich_ip_returns_placeholder():
    result = enrich_ip("185.220.101.1")
    assert result.ioc_type == "ip"
    assert result.ioc_value == "185.220.101.1"


def test_enrich_hash_returns_placeholder():
    result = enrich_hash("44d88612fea8a8f36de82e1278abb02f")
    assert result.ioc_type == "hash"


def test_enrich_domain_returns_placeholder():
    result = enrich_domain("malicious-domain-example.com")
    assert result.ioc_type == "domain"