# Threat Intelligence API Reference

## AbuseIPDB
- Sign up: https://www.abuseipdb.com/register
- Auth method: API key in `Key` header
- Free tier limit: 1,000 checks/day
- Endpoint: `GET https://api.abuseipdb.com/api/v2/check`

## VirusTotal
- Sign up: https://www.virustotal.com/gui/join-us
- Auth method: API key in `x-apikey` header
- Free tier limit: 4 requests/min, 500/day
- Endpoint: `GET https://www.virustotal.com/api/v3/files/{hash}`

## MaxMind GeoLite2
- Sign up: https://www.maxmind.com/en/geolite2/signup
- Auth method: Download local `.mmdb` database (no key needed for offline lookups)
- No rate limit for local DB use

## Environment Variables Needed (add to `.env`, never commit)
```
ABUSEIPDB_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here
GEOLITE2_DB_PATH=./data/GeoLite2-City.mmdb
```