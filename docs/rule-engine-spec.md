# Rule Engine Specification — Severity to Action Mapping

## Purpose
Defines how a computed risk score (0-100) maps to an automated containment action.
This spec drives the Playbook Engine built in Week 3.

## Risk Score Bands

| Risk Score | Severity | Action |
|---|---|---|
| 0–30 | Low | Log only, no containment action |
| 31–70 | Medium | Notify analyst, tag incident for review |
| 71–100 | High | Auto-trigger containment (block IP / isolate host) |


## Action Types
- `LOG_ONLY` — record the alert, take no automated action
- `NOTIFY_ANALYST` — flag incident in dashboard, no auto-containment
- `BLOCK_IP` — trigger mock firewall to block the source IP
- `ISOLATE_HOST` — trigger mock EDR to quarantine the affected host
- `AWS_SG_ISOLATE` — trigger simulated AWS Security Group rule to cut off traffic

## Playbook YAML Shape (used starting Week 3)
```yaml
name: malicious_ip_playbook
trigger:
  risk_score_min: 71
  ioc_type: ip
actions:
  - type: BLOCK_IP
    target: "{{ ioc_value }}"
  - type: NOTIFY_ANALYST
    message: "High-risk IP auto-blocked: {{ ioc_value }}"
