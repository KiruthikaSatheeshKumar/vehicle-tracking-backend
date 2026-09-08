from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class GPSCreate(BaseModel):
    vehicle_id: int
    latitude: float
    longitude: float
    timestamp: datetime
    speed: float = 0

class LocationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    latitude: float
    longitude: float
    timestamp: datetime
    speed: float

class VehicleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    vehicle_code: str
    registration_number: str
    status: str

class RoutePointOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    latitude: float
    longitude: float
    sequence: int

class RouteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    start_point: str
    end_point: str
    points: list[RoutePointOut]
    
class TrackingResponse(BaseModel):
    route: RouteOut
    vehicle: VehicleOut
    current_location: LocationOut | None
