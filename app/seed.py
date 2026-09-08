from .database import Base, engine, SessionLocal
from .models import User, Route, RoutePoint, Vehicle
from .auth import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count():
            return
        route_a = Route(name="Route A", start_point="Central Station", end_point="Tech Park")
        route_b = Route(name="Route B", start_point="Airport", end_point="City Center")
        db.add_all([route_a, route_b]); db.flush()

        for seq, (lat, lon) in enumerate([(13.0827,80.2707),(13.0850,80.2750),(13.0900,80.2800),(13.0950,80.2850)]):
            db.add(RoutePoint(route_id=route_a.id, sequence=seq, latitude=lat, longitude=lon))
        for seq, (lat, lon) in enumerate([(12.9941,80.1709),(13.0000,80.1800),(13.0150,80.1950),(13.0300,80.2100)]):
            db.add(RoutePoint(route_id=route_b.id, sequence=seq, latitude=lat, longitude=lon))

        bus1 = Vehicle(vehicle_code="BUS-001", registration_number="TN01AB0001", status="moving")
        bus2 = Vehicle(vehicle_code="BUS-002", registration_number="TN01AB0002", status="stopped")
        db.add_all([bus1,bus2]); db.flush()
        db.add_all([
            User(username="usera", password_hash=hash_password("password123"), route_id=route_a.id, vehicle_id=bus1.id),
            User(username="userb", password_hash=hash_password("password123"), route_id=route_b.id, vehicle_id=bus2.id),
        ])
        db.commit()
    finally:
        db.close()
