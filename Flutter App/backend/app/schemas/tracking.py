from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RouteResponse(BaseModel):
    id: int
    name: str
    code: str
    start_name: str
    end_name: str
    polyline: str

    model_config = {"from_attributes": True}


class VehicleResponse(BaseModel):
    id: int
    vehicle_code: str
    plate_number: str
    status: str
    route_id: int

    model_config = {"from_attributes": True}


class AssignmentResponse(BaseModel):
    user_id: int
    full_name: str
    route: RouteResponse
    vehicle: VehicleResponse


class GpsIngestRequest(BaseModel):
    vehicle_id: int
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    speed: float = Field(default=0, ge=0)
    timestamp: datetime | None = None


class GpsPointResponse(BaseModel):
    id: int
    vehicle_id: int
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

    model_config = {"from_attributes": True}

