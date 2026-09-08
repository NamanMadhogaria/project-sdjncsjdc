from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.tracking import User
from app.schemas.tracking import (
    AssignmentResponse,
    GpsIngestRequest,
    GpsPointResponse,
    LoginRequest,
    TokenResponse,
    VehicleResponse,
)
from app.services.tracking import (
    create_gps_point,
    ensure_user_assignment,
    history_for_user,
    latest_location_for_user,
)

router = APIRouter(prefix="/api")


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalars(select(User).where(User.email == payload.email)).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    return TokenResponse(access_token=create_access_token(user.email))


@router.get("/me/assignment", response_model=AssignmentResponse)
def my_assignment(user: User = Depends(get_current_user)) -> AssignmentResponse:
    ensure_user_assignment(user)
    return AssignmentResponse(
        user_id=user.id,
        full_name=user.full_name,
        route=user.route,
        vehicle=user.vehicle,
    )


@router.get("/me/vehicle", response_model=VehicleResponse)
def my_vehicle(user: User = Depends(get_current_user)) -> VehicleResponse:
    ensure_user_assignment(user)
    return user.vehicle


@router.get("/me/location/latest", response_model=GpsPointResponse)
def my_latest_location(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> GpsPointResponse:
    return latest_location_for_user(db, user)


@router.get("/me/location/history", response_model=list[GpsPointResponse])
def my_location_history(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[GpsPointResponse]:
    return history_for_user(db, user, limit=limit)


@router.post("/gps", response_model=GpsPointResponse, status_code=status.HTTP_201_CREATED)
def ingest_gps(
    payload: GpsIngestRequest, db: Session = Depends(get_db)
) -> GpsPointResponse:
    return create_gps_point(db, payload)

