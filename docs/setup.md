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

## Secrets Management

Never commit real API keys. All secrets live in a local `.env` file (already gitignored).

1. Copy the example file:
```bash
   cp .env.example backend/.env
```
2. Fill in your real keys in `backend/.env`:

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