from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.tracking import GpsPoint, User, Vehicle
from app.schemas.tracking import GpsIngestRequest


def ensure_user_assignment(user: User) -> None:
    if not user.route_id or not user.vehicle_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No route and vehicle assignment found for this user.",
        )
    if user.vehicle.route_id != user.route_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User route and vehicle assignment mismatch.",
        )


def create_gps_point(db: Session, payload: GpsIngestRequest) -> GpsPoint:
    vehicle = db.get(Vehicle, payload.vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    point = GpsPoint(
        vehicle_id=payload.vehicle_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        speed=payload.speed,
        timestamp=payload.timestamp or datetime.now(timezone.utc),
    )
    db.add(point)
    db.commit()
    db.refresh(point)
    return point


def latest_location_for_user(db: Session, user: User) -> GpsPoint:
    ensure_user_assignment(user)
    point = db.scalars(
        select(GpsPoint)
        .where(GpsPoint.vehicle_id == user.vehicle_id)
        .order_by(desc(GpsPoint.timestamp))
        .limit(1)
    ).first()
    if point is None:
        raise HTTPException(status_code=404, detail="No GPS data found.")
    return point


def history_for_user(db: Session, user: User, limit: int = 100) -> list[GpsPoint]:
    ensure_user_assignment(user)
    return list(
        db.scalars(
            select(GpsPoint)
            .where(GpsPoint.vehicle_id == user.vehicle_id)
            .order_by(desc(GpsPoint.timestamp))
            .limit(limit)
        )
    )

