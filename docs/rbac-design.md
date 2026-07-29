# RBAC Design — Roles and Permissions

## Roles

| Role | Description |
|---|---|
| Admin | Full access — manages users/roles, all Analyst permissions |
| Analyst | Can view everything, re-run playbooks, release containment |
| Viewer | Read-only access to incidents and IoCs |

## Permission Matrix

| Permission | Admin | Analyst | Viewer |
|---|---|---|---|
| view_incidents | ✅ | ✅ | ✅ |
| view_iocs | ✅ | ✅ | ✅ |
| rerun_playbook | ✅ | ✅ | ❌ |
| release_containment | ✅ | ✅ | ❌ |
| manage_users | ✅ | ❌ | ❌ |
| manage_rbac | ✅ | ❌ | ❌ |

## Enforcement Plan (Week 4)
- JWT token will carry the user's role as a claim
- A FastAPI dependency (`require_permission("rerun_playbook")`) will check
  `has_permission()` before allowing the route to execute
- Dashboard UI will hide/disable buttons the current role can't use