# Architecture

## Backend

The backend is organized as a modular FastAPI app:

- `app/main.py` creates the FastAPI application.
- `app/api/` contains route handlers.
- `app/core/` contains configuration and security helpers.
- `app/db/` contains SQLAlchemy database setup and seed data.
- `app/models/` contains database models.
- `app/schemas/` contains Pydantic request and response models.
- `app/services/` contains reusable business logic.

## Database Design

### users

- `id`
- `email`
- `hashed_password`
- `full_name`
- `route_id`
- `vehicle_id`
- `is_active`

### routes

- `id`
- `name`
- `code`
- `start_name`
- `end_name`
- `polyline`

### vehicles

- `id`
- `vehicle_code`
- `plate_number`
- `status`
- `route_id`

### gps_points

- `id`
- `vehicle_id`
- `latitude`
- `longitude`
- `speed`
- `timestamp`
- `created_at`

## Authorization Model

The JWT token identifies the current user. Assignment checks are performed in backend services before returning route, vehicle, current location, or history data.

A user can access a vehicle only when:

- `user.vehicle_id == vehicle.id`
- `user.route_id == vehicle.route_id`

The Flutter app never decides access by itself. It only displays data returned by authorized backend APIs.

## GPS Data Flow

1. A vehicle or simulator sends GPS data.
2. FastAPI validates the vehicle ID and GPS payload.
3. The GPS point is stored in `gps_points`.
4. Latest location is derived from the newest GPS point for the vehicle.
5. Authenticated users query only their assigned vehicle's latest or historical points.

## API Endpoints

- `POST /api/auth/login`
- `GET /api/me/assignment`
- `GET /api/me/vehicle`
- `GET /api/me/location/latest`
- `GET /api/me/location/history`
- `POST /api/gps`
- `GET /health`

