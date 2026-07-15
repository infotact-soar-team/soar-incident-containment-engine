"""
Mock Firewall API — simulates blocking/unblocking IPs.
No real firewall is touched; state is kept in memory for demo purposes.
"""

_blocked_ips = set()

def block_ip(ip: str) -> dict:
    _blocked_ips.add(ip)
    return {
        "action": "BLOCK_IP",
        "ip": ip,
        "status": "blocked",
        "success": True,
    }

def unblock_ip(ip: str) -> dict:
    _blocked_ips.discard(ip)
    return {
        "action": "UNBLOCK_IP",
        "ip": ip,
        "status": "unblocked",
        "success": True,
    }

def is_blocked(ip: str) -> bool:
    return ip in _blocked_ips

def list_blocked_ips() -> list:
    return list(_blocked_ips)
