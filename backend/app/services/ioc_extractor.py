import re

IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN_REGEX = re.compile(r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b")
MD5_REGEX = re.compile(r"\b[a-fA-F0-9]{32}\b")
SHA1_REGEX = re.compile(r"\b[a-fA-F0-9]{40}\b")
SHA256_REGEX = re.compile(r"\b[a-fA-F0-9]{64}\b")


def extract_iocs(text: str) -> dict:
    """
    Scans free-text (alert message/description) and extracts
    IP addresses, domains, and file hashes (MD5/SHA1/SHA256).
    Returns a dict grouped by IoC type.
    """
    ips = IP_REGEX.findall(text)

    # Find hashes first so domain regex doesn't misfire on hash-like strings
    sha256_hashes = SHA256_REGEX.findall(text)
    sha1_hashes = SHA1_REGEX.findall(text)
    md5_hashes = MD5_REGEX.findall(text)

    domains = [
        d for d in DOMAIN_REGEX.findall(text)
        if d not in ips  # avoid IPs being misread as domains
    ]

    return {
        "ip": list(set(ips)),
        "domain": list(set(domains)),
        "hash": list(set(sha256_hashes + sha1_hashes + md5_hashes)),
    }