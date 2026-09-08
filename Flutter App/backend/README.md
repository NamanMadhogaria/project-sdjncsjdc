# Backend - GPS Vehicle Tracking API

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The API will run at `http://localhost:8000`.

## Demo Users

- `usera@example.com` / `password123` -> Route A, BUS-001
- `userb@example.com` / `password123` -> Route B, BUS-002

## API Endpoints

### Login

`POST /api/auth/login`

```json
{
  "email": "usera@example.com",
  "password": "password123"
}
```

### Assigned Route and Vehicle

`GET /api/me/assignment`

Requires bearer token.

### Vehicle Details

`GET /api/me/vehicle`

Requires bearer token.

### Latest Location

`GET /api/me/location/latest`

Requires bearer token.

### Historical Tracking

`GET /api/me/location/history?limit=100`

Requires bearer token.

### GPS Ingestion

`POST /api/gps`

```json
{
  "vehicle_id": 1,
  "latitude": 12.9716,
  "longitude": 77.5946,
  "speed": 25,
  "timestamp": "2026-09-05T12:00:00Z"
}
```

## Docker Compose

```bash
cd backend
docker compose up --build
```

This starts PostgreSQL, Mosquitto MQTT, the FastAPI API, and a GPS simulator that publishes to MQTT topics like `vehicles/1/gps`.

## Authorization Logic

The backend reads the authenticated user from the JWT token and uses the user's `route_id` and `vehicle_id` assignment for all `/api/me/*` endpoints. Users never pass route IDs or vehicle IDs when reading tracking data, which prevents User A from requesting User B's vehicle.
