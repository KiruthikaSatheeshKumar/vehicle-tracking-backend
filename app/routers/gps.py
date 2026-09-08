from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import GPSData, Vehicle
from ..schemas import GPSCreate, LocationOut

router = APIRouter()

@router.post("/ingest", response_model=LocationOut)
def ingest(data: GPSCreate, db: Session = Depends(get_db)):
    vehicle = db.get(Vehicle, data.vehicle_id)
    if not vehicle:
        raise HTTPException(404, "Vehicle not found")
    db.query(GPSData).filter(GPSData.vehicle_id == vehicle.id).update({GPSData.is_latest: 0})
    point = GPSData(**data.model_dump(), is_latest=1)
    vehicle.status = "moving" if data.speed > 0 else "stopped"
    db.add(point); db.commit(); db.refresh(point)
    return point
