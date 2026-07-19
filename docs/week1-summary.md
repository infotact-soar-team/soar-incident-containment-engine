# Week 1 Summary — Webhook Ingestion & Data Normalization

## Completed
- Webhook ingestion endpoint (`/webhook/alert`)
- Alert normalization (severity mapping, timestamp parsing)
- IoC extraction (IP, domain, hash)
- Redis connection + generic caching wrapper
- Enrichment service skeleton (ready for Week 2 live integrations)
- Playbook schema + YAML loader
- Mock Firewall, Mock EDR, and AWS Security Group (moto) simulations
- Structured logging + global exception handling
- GitHub Actions CI pipeline with test coverage reporting

## Test Coverage
Run locally via:
```bash
cd backend
pytest -v --cov=app --cov-report=term-missing
```

## Known Gaps Going Into Week 2
- Enrichment functions are placeholders — live AbuseIPDB/VirusTotal/GeoIP calls start Week 2
- No rule engine yet — playbooks are triggered manually in tests, automatic triggering is Week 3
- No RBAC/auth yet — all endpoints currently open, addressed in Week 4