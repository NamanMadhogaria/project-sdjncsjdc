# Full Stack Flutter + Python GPS Tracking Assessment

## Task Summary

Build a GPS-based vehicle tracking system with:

- A Python FastAPI backend.
- A Flutter mobile application.
- A relational database using PostgreSQL or MySQL.
- Vehicle GPS ingestion through MQTT, REST API, or another suitable approach.

This implementation uses FastAPI, PostgreSQL, JWT authentication, REST GPS ingestion, optional MQTT ingestion, Docker Compose, and a Flutter mobile app.

## Core Business Flow

User -> Assigned Route -> Assigned Vehicle -> GPS Data -> FastAPI -> Database -> Flutter App

Each user is assigned exactly one bus route and one vehicle. The backend enforces that authenticated users can only access their own assigned route, vehicle, latest vehicle location, and historical tracking data.

## Backend Requirements

- Support multiple user logins.
- Authenticate users with JWT access tokens.
- Store users, bus routes, vehicles, and GPS tracking data.
- Assign one route and one vehicle to each user.
- Receive GPS updates from vehicles.
- Store latitude, longitude, timestamp, speed, and vehicle ID.
- Maintain latest vehicle location and historical GPS records.
- Provide APIs for:
  - Login.
  - Assigned route.
  - Assigned vehicle.
  - Current location.
  - Historical tracking data.
- Enforce authorization in the backend.
- Keep the architecture modular and production-ready.

## Flutter Requirements

- Login screen.
- Home/tracking screen.
- Display assigned route, assigned vehicle, latest GPS location, and vehicle status.
- Map view for route and current vehicle location.
- Loading and API error states.

## Bonus Scope

- Dockerize backend, PostgreSQL, and MQTT broker.
- Provide a simple GPS simulator that can publish coordinates to MQTT.

