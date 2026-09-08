# Vehicle Tracking Backend

FastAPI + PostgreSQL + MQTT backend for the GPS vehicle tracking assessment.

## Run with Docker
```bash
docker compose up --build
```
API: http://localhost:8000  
Swagger: http://localhost:8000/docs

## Demo accounts
- `usera` / `password123` → Route A → BUS-001
- `userb` / `password123` → Route B → BUS-002

## GPS
REST:
```bash
curl -X POST http://localhost:8000/api/gps/ingest -H "Content-Type: application/json" -d "{"vehicle_id":1,"latitude":13.0827,"longitude":80.2707,"timestamp":"2026-09-07T12:00:00Z","speed":25}"
```

MQTT topic: `vehicles/{vehicle_id}/gps`

Run simulator locally after starting Docker:
```bash
pip install -r requirements.txt
python simulator/gps_simulator.py
```

## Architecture
User → JWT Authentication → Assignment-aware APIs → PostgreSQL  
Vehicle → MQTT GPS → FastAPI subscriber → GPS history + latest location → Flutter

Backend authorization derives the route and vehicle from the authenticated user, so changing IDs in a client request cannot expose another user's vehicle.
