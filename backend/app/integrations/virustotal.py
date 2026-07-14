
"""
VirusTotal Integration (skeleton - live implementation in Week 2)
Docs: https://developers.virustotal.com/reference/overview
Auth: API key via header 'x-apikey'
Rate limit (free tier): 4 requests/min, 500/day
"""


def check_hash(file_hash: str) -> dict:
    """
    Look up a file hash (MD5/SHA1/SHA256) reputation via VirusTotal.
    To be implemented in Week 2.
    """
    raise NotImplementedError("VirusTotal live integration pending - Week 2")


def check_domain(domain: str) -> dict:
    """
    Look up a domain's reputation via VirusTotal.
    To be implemented in Week 2.
    """
    raise NotImplementedError("VirusTotal live integration pending - Week 2")