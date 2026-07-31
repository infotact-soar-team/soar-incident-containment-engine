# Local Development Setup

## Prerequisites
- Python 3.13 or Python 3.14 (the standard, non-free-threaded build)
- Docker Desktop, or PostgreSQL 16 and Redis installed locally

## Start local services with Docker

From the repository root:

```bash
docker compose up -d
```

This starts PostgreSQL on port 5432 and Redis on port 6379 with the development
credentials in `backend/.env.example`.

## Windows
1. Install PostgreSQL: https://www.postgresql.org/download/windows/
2. Install Redis (via Memurai or WSL): https://www.memurai.com/
3. Create the database:

## Running the App
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000/health`

## Secrets Management

Never commit real API keys. All secrets live in a local `.env` file (already gitignored).

1. Copy the example file:
```powershell
Copy-Item backend/.env.example backend/.env
```
2. Fill in your real keys in `backend/.env`. Use `SOAR_DEBUG=true` or
   `SOAR_DEBUG=false` to control debug mode.

3. Never run `git add .env` — confirm it's ignored:
```bash
   git check-ignore backend/.env
```
   This should print the path back, confirming it's ignored.

   ## GeoLite2 Database Setup

1. Sign up (free): https://www.maxmind.com/en/geolite2/signup
2. Download GeoLite2-City.mmdb
3. Place it at backend/data/GeoLite2-City.mmdb (create the data/ folder if needed)
4. Confirm .env has:

   GEOLITE2_DB_PATH=./data/GeoLite2-City.mmdb

   ## Running the Celery Worker (for async enrichment tasks)

Once Redis is running locally, start a worker in a separate terminal:

```bash
cd backend
celery -A app.core.celery_app worker --loglevel=info
```

Windows users: add `--pool=solo` since Celery's default pool doesn't support Windows well:
```bash
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```
