import json, math, time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
ROUTES = {
    1: [(13.0827,80.2707),(13.0850,80.2750),(13.0900,80.2800),(13.0950,80.2850)],
    2: [(12.9941,80.1709),(13.0000,80.1800),(13.0150,80.1950),(13.0300,80.2100)]
}
client = mqtt.Client()
client.connect(BROKER, PORT, 60)
i = 0
while True:
    for vehicle_id, points in ROUTES.items():
        lat, lon = points[i % len(points)]
        payload = {"vehicle_id": vehicle_id, "latitude": lat, "longitude": lon,
                   "timestamp": datetime.now(timezone.utc).isoformat(), "speed": 24.0}
        client.publish(f"vehicles/{vehicle_id}/gps", json.dumps(payload))
    i += 1
    time.sleep(5)
