"""
RBAC role definitions. Enforcement (route guards) comes in Week 4 —
this just defines the roles and their permitted actions so everyone
builds against the same model.
"""
from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


ROLE_PERMISSIONS = {
    Role.ADMIN: {
        "view_incidents", "view_iocs", "rerun_playbook",
        "release_containment", "manage_users", "manage_rbac",
    },
    Role.ANALYST: {
        "view_incidents", "view_iocs", "rerun_playbook", "release_containment",
    },
    Role.VIEWER: {
        "view_incidents", "view_iocs",
    },
}


def has_permission(role: Role, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())