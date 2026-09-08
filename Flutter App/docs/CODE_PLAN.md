# Code Plan

## Phase 1 - Backend

1. Create FastAPI app structure.
2. Add SQLAlchemy models for users, routes, vehicles, and GPS points.
3. Add JWT authentication.
4. Add seed data for two demo users, two routes, and two buses.
5. Implement assignment-based authorization.
6. Implement GPS ingestion and tracking APIs.
7. Add Dockerfile, Docker Compose, and MQTT simulator.

## Phase 2 - Flutter

1. Create Flutter project metadata and dependencies.
2. Add API client with token handling.
3. Add typed models for login, assignment, vehicle, and GPS data.
4. Build login screen.
5. Build tracking screen with refresh, route info, vehicle status, and location history.
6. Build map screen using `flutter_map` and OpenStreetMap tiles.
7. Add error and loading states.

## Phase 3 - Verification

1. Run backend dependency installation.
2. Run backend tests or syntax checks.
3. Flutter cannot be run in this environment because Flutter is not installed.
4. Docker Compose cannot be run in this environment because Docker is not installed.

