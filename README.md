# SOAR Incident Containment Engine

A Python‑based Security Orchestration, Automation, and Response (SOAR) platform that ingests SIEM alerts, enriches Indicators of Compromise (IoCs) using external threat intelligence APIs, and executes automated playbooks to contain threats in under 5 seconds.

---

## 🚀 Project Overview
This project aims to reduce Mean Time to Respond (MTTR) for enterprise cloud environments by automating alert triage and containment. It integrates FastAPI for alert ingestion, AbuseIPDB and VirusTotal for enrichment, and custom playbooks for rapid isolation of compromised assets.

---

## 🧩 Core Features
- **FastAPI Listener** – Receives SIEM alerts in real time.  
- **Threat Enrichment** – Queries AbuseIPDB and VirusTotal for IoC reputation.  
- **Playbook Automation** – Executes containment actions (e.g., AWS EC2 isolation, firewall IP blocking).  
- **Case Management Dashboard** – Tracks incidents with Role‑Based Access Control (RBAC).  
- **Audit Logging** – Maintains traceability for all automated actions.

---

## 🛠️ Engineering Roadmap
| Week | Focus Area | Deliverables |
|------|-------------|--------------|
| 1 | Alert ingestion & normalization | FastAPI webhook setup |
| 2 | Threat enrichment | API integration modules |
| 3 | Playbook automation | AWS & firewall orchestration |
| 4 | Dashboard & RBAC | Web interface and access control |

---

## 🧑‍💻 Version Control Standards
- Each team member works on a dedicated branch (`mahendra-dev`, `hardik-dev`, `kanishk-dev`, `praveen-dev`).  
- Pull Requests are mandatory for merging into `main`.  
- Use semantic commit messages (`feat:`, `fix:`, `docs:`).  
- No hardcoded secrets — use environment variables or GitHub Secrets.

---

## 📊 Evaluation Compliance
- **Mid Review:** Minimum 10 days of commits in the last 14 days.  
- **Final Review:** Continuous commits for 20 days without gaps.  
- Weekly updates submitted via the Infotact Dashboard.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---

## 👥 Contributors
Team Lead:  **Hardik Jain**  
Members:**Kanishk Soni**, **Praveen CS**, **Mahendra Marisa**

---

## 🧠 Organization
**Infotact Solutions – Cyber Security Batch 18 Group 2**  
GitHub Organization: [infotact‑soar‑team](https://github.com/infotact-soar-team)
