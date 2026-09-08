import json
import threading
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from .config import settings
from .database import SessionLocal
from .models import GPSData, Vehicle

def save_gps(payload: dict):
    required = ["vehicle_id", "latitude", "longitude", "timestamp"]
    if any(k not in payload for k in required):
        return
    db: Session = SessionLocal()
    try:
        vehicle = db.get(Vehicle, int(payload["vehicle_id"]))
        if not vehicle:
            return
        db.query(GPSData).filter(GPSData.vehicle_id == vehicle.id).update({GPSData.is_latest: 0})
        ts = datetime.fromisoformat(str(payload["timestamp"]).replace("Z", "+00:00"))
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        point = GPSData(vehicle_id=vehicle.id, latitude=float(payload["latitude"]),
                        longitude=float(payload["longitude"]), timestamp=ts,
                        speed=float(payload.get("speed", 0)), is_latest=1)
        vehicle.status = "moving" if float(payload.get("speed", 0)) > 0 else "stopped"
        db.add(point)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def start_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties=None):
        client.subscribe(settings.mqtt_topic)
    def on_message(client, userdata, msg):
        try:
            save_gps(json.loads(msg.payload.decode()))
        except Exception:
            pass
    def run():
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(settings.mqtt_host, settings.mqtt_port, 60)
            client.loop_forever()
        except Exception:
            # REST ingestion still works if MQTT is temporarily unavailable.
            pass
    threading.Thread(target=run, daemon=True).start()
