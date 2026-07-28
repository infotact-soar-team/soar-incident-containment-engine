# Dashboard Wireframe — Incident & Action Timeline (Week 4 Prep)

## Purpose
Defines the UI layout and the API data shape the dashboard will consume,
so Incident/Action models (built Day 1) and future APIs (Week 4) match
what the frontend actually needs.

## Screen 1 — Incident List
┌─────────────────────────────────────────────────────────┐
│ Incidents [Filter ▾] │
├─────────┬──────────┬──────────┬──────────┬──────────────┤
│ Severity│ Source │ Status │ Created │ Actions Taken │
├─────────┼──────────┼──────────┼──────────┼──────────────┤
│ 🔴 High │ Splunk │ Open │ 2m ago │ 2 actions │
│ 🟡 Med │ Wazuh │ Progress │ 15m ago │ 1 action │
│ 🟢 Low │ Splunk │ Closed │ 1h ago │ 0 actions │
└─────────┴──────────┴──────────┴──────────┴──────────────┘

Required API: `GET /incidents?severity=&status=&limit=&offset=`

## Screen 2 — Incident Detail + Timeline

┌─────────────────────────────────────────────────────────┐
│ Incident 
#abc123 — High Severity │
│ IoC: 185.220.101.1 (ip) | Risk Score: 92 │
├─────────────────────────────────────────────────────────┤
│ Timeline │
│ ● 10:00:01 — Alert received (Splunk) │
│ ● 10:00:02 — IoC extracted: 185.220.101.1 │
│ ● 10:00:03 — Enrichment complete: risk_score=92 │
│ ● 10:00:04 — Playbook triggered: malicious_ip_playbook │
│ ● 10:00:05 — Action: BLOCK_IP -> success │
│ ● 10:00:05 — Action: NOTIFY_ANALYST -> success │
└─────────────────────────────────────────────────────────┘

Required API: `GET /incidents/{id}/actions` returning Action rows ordered by `executed_at`.

## Screen 3 — Manual Override

┌─────────────────────────────────────────────────────────┐
│ [ Re-run Playbook ] [ Release Containment ] │
└─────────────────────────────────────────────────────────┘

Required API: `POST /incidents/{id}/rerun` (Week 4, RBAC-gated to Analyst/Admin).

## API Contract Summary (for Hardik/Mahendra reference)
| Endpoint | Returns |
|---|---|
| GET /incidents | List of Incident rows with basic Alert fields joined |
| GET /incidents/{id}/actions | List of Action rows for that incident, ordered by time |
| POST /incidents/{id}/rerun | Triggers PlaybookEngine again for that incident's IoC |