from app.services.ioc_extractor import extract_iocs


def test_extract_ip():
    text = "Suspicious connection from 185.220.101.1 detected"
    result = extract_iocs(text)
    assert "185.220.101.1" in result["ip"]


def test_extract_domain():
    text = "Beaconing to malicious-domain-example.com observed"
    result = extract_iocs(text)
    assert "malicious-domain-example.com" in result["domain"]


def test_extract_hash():
    text = "File hash 44d88612fea8a8f36de82e1278abb02f flagged as malware"
    result = extract_iocs(text)
    assert "44d88612fea8a8f36de82e1278abb02f" in result["hash"]


def test_extract_multiple_types():
    text = "IP 1.2.3.4 contacted evil.com and dropped 44d88612fea8a8f36de82e1278abb02f"
    result = extract_iocs(text)
    assert result["ip"] and result["domain"] and result["hash"]


def test_extract_nothing_when_clean():
    text = "System rebooted normally"
    result = extract_iocs(text)
    assert result["ip"] == [] and result["domain"] == [] and result["hash"] == []