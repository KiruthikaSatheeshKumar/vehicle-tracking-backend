from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, GPSData, Vehicle
from ..schemas import RouteOut, VehicleOut, TrackingResponse, LocationOut
from ..auth import get_current_user

router = APIRouter()

def assigned(user, db):
    if not user.route_id or not user.vehicle_id:
        raise HTTPException(404, "No route/vehicle assigned")
    route = user.route
    vehicle = user.vehicle
    if not route or not vehicle:
        raise HTTPException(404, "Assigned route/vehicle not found")
    return route, vehicle

@router.get("/me/tracking", response_model=TrackingResponse)
def my_tracking(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    route, vehicle = assigned(user, db)

    latest = db.query(GPSData).filter(
        GPSData.vehicle_id == vehicle.id,
        GPSData.is_latest == 1
    ).first()

    return TrackingResponse(
        route=RouteOut.model_validate(route),
        vehicle=VehicleOut.model_validate(vehicle),
        current_location=LocationOut.model_validate(latest) if latest else None
    )

@router.get("/me/route", response_model=RouteOut)
def my_route(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    route, _ = assigned(user, db)
    return route

@router.get("/me/vehicle", response_model=VehicleOut)
def my_vehicle(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _, vehicle = assigned(user, db)
    return vehicle

@router.get("/me/location", response_model=LocationOut | None)
def my_location(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _, vehicle = assigned(user, db)
    latest = db.query(GPSData).filter(GPSData.vehicle_id == vehicle.id, GPSData.is_latest == 1).first()
    return LocationOut.model_validate(latest) if latest else None

@router.get("/me/history", response_model=list[LocationOut])
def my_history(
    limit: int = Query(50, ge=1, le=500),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    _, vehicle = assigned(user, db)
    rows = (db.query(GPSData).filter(GPSData.vehicle_id == vehicle.id)
            .order_by(GPSData.timestamp.desc()).limit(limit).all())
    return [LocationOut.model_validate(x) for x in rows]
