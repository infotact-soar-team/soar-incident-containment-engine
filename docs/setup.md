# Local Development Setup (No Docker)

## Prerequisites
- Python 3.13
- PostgreSQL 16 installed locally and running
- Redis installed locally and running

## Windows
1. Install PostgreSQL: https://www.postgresql.org/download/windows/
2. Install Redis (via Memurai or WSL): https://www.memurai.com/
3. Create the database:

## Running the App
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000/health`