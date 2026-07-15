"""
Mock EDR API — simulates host isolation/quarantine actions.
No real EDR agent is touched; state is kept in memory for demo purposes.
"""

_isolated_hosts = set()


def isolate_host(hostname: str) -> dict:
    _isolated_hosts.add(hostname)
    return {
        "action": "ISOLATE_HOST",
        "hostname": hostname,
        "status": "isolated",
        "success": True,
    }


def release_host(hostname: str) -> dict:
    _isolated_hosts.discard(hostname)
    return {
        "action": "RELEASE_HOST",
        "hostname": hostname,
        "status": "released",
        "success": True,
    }


def is_isolated(hostname: str) -> bool:
    return hostname in _isolated_hosts


def list_isolated_hosts() -> list:
    return list(_isolated_hosts)
