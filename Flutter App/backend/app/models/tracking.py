from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    start_name: Mapped[str] = mapped_column(String(120), nullable=False)
    end_name: Mapped[str] = mapped_column(String(120), nullable=False)
    polyline: Mapped[str] = mapped_column(Text, nullable=False)

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="route")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehicle_code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    plate_number: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active")
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))

    route: Mapped[Route] = relationship(back_populates="vehicles")
    gps_points: Mapped[list["GpsPoint"]] = relationship(back_populates="vehicle")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    route: Mapped[Route] = relationship()
    vehicle: Mapped[Vehicle] = relationship()


class GpsPoint(Base):
    __tablename__ = "gps_points"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    speed: Mapped[float] = mapped_column(Float, default=0)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    vehicle: Mapped[Vehicle] = relationship(back_populates="gps_points")

