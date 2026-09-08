from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    route = relationship("Route", foreign_keys=[route_id])
    vehicle = relationship("Vehicle", foreign_keys=[vehicle_id])

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    start_point = Column(String(120), nullable=False)
    end_point = Column(String(120), nullable=False)
    points = relationship("RoutePoint", cascade="all, delete-orphan", order_by="RoutePoint.sequence")

class RoutePoint(Base):
    __tablename__ = "route_points"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    vehicle_code = Column(String(50), unique=True, nullable=False, index=True)
    registration_number = Column(String(50), nullable=False)
    status = Column(String(30), default="offline")
    latest_location = relationship("GPSData", uselist=False, primaryjoin="and_(Vehicle.id==GPSData.vehicle_id, GPSData.is_latest==True)", foreign_keys="GPSData.vehicle_id")
    gps_history = relationship("GPSData", cascade="all, delete-orphan", back_populates="vehicle")

class GPSData(Base):
    __tablename__ = "gps_data"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    speed = Column(Float, default=0)
    is_latest = Column(Integer, default=0, index=True)
    vehicle = relationship("Vehicle", back_populates="gps_history")
