from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.tracking import GpsPoint, Route, User, Vehicle


def seed_demo_data(db: Session) -> None:
    if db.scalars(select(User)).first():
        return

    route_a = Route(
        name="Route A - Central Loop",
        code="ROUTE-A",
        start_name="Central Station",
        end_name="Tech Park",
        polyline="12.9716,77.5946;12.9760,77.5993;12.9810,77.6100",
    )
    route_b = Route(
        name="Route B - Airport Express",
        code="ROUTE-B",
        start_name="City Center",
        end_name="Airport Road",
        polyline="12.9352,77.6245;12.9500,77.6400;12.9800,77.7000",
    )
    db.add_all([route_a, route_b])
    db.flush()

    bus_001 = Vehicle(
        vehicle_code="BUS-001",
        plate_number="KA-01-AA-1001",
        status="active",
        route_id=route_a.id,
    )
    bus_002 = Vehicle(
        vehicle_code="BUS-002",
        plate_number="KA-01-AA-1002",
        status="active",
        route_id=route_b.id,
    )
    db.add_all([bus_001, bus_002])
    db.flush()

    db.add_all(
        [
            User(
                email="usera@example.com",
                hashed_password=hash_password("password123"),
                full_name="User A",
                route_id=route_a.id,
                vehicle_id=bus_001.id,
            ),
            User(
                email="userb@example.com",
                hashed_password=hash_password("password123"),
                full_name="User B",
                route_id=route_b.id,
                vehicle_id=bus_002.id,
            ),
        ]
    )
    now = datetime.now(timezone.utc)
    db.add_all(
        [
            GpsPoint(
                vehicle_id=bus_001.id,
                latitude=12.9716,
                longitude=77.5946,
                speed=24.5,
                timestamp=now,
            ),
            GpsPoint(
                vehicle_id=bus_002.id,
                latitude=12.9352,
                longitude=77.6245,
                speed=32.0,
                timestamp=now,
            ),
        ]
    )
    db.commit()

