import math
import os
import time
from datetime import datetime, timezone
import json

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))


def publish_point(
    client: mqtt.Client, vehicle_id: int, base_lat: float, base_lng: float, step: int
) -> None:
    payload = {
        "latitude": base_lat + math.sin(step / 10) * 0.01,
        "longitude": base_lng + math.cos(step / 10) * 0.01,
        "speed": 25 + math.sin(step / 5) * 8,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    client.publish(f"vehicles/{vehicle_id}/gps", json.dumps(payload))


def main() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()
    step = 0
    while True:
        publish_point(client, 1, 12.9716, 77.5946, step)
        publish_point(client, 2, 12.9352, 77.6245, step)
        step += 1
        time.sleep(5)


if __name__ == "__main__":
    main()
