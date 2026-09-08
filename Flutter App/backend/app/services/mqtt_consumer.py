import json
import threading
from datetime import datetime

import paho.mqtt.client as mqtt

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.schemas.tracking import GpsIngestRequest
from app.services.tracking import create_gps_point


def start_mqtt_consumer() -> None:
    settings = get_settings()
    if not settings.enable_mqtt:
        return

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(client, userdata, flags, reason_code, properties) -> None:
        client.subscribe(settings.mqtt_topic)

    def on_message(client, userdata, message) -> None:
        try:
            payload = json.loads(message.payload.decode("utf-8"))
            parts = message.topic.split("/")
            vehicle_id = int(payload.get("vehicle_id") or parts[1])
            timestamp = payload.get("timestamp")
            gps_payload = GpsIngestRequest(
                vehicle_id=vehicle_id,
                latitude=payload["latitude"],
                longitude=payload["longitude"],
                speed=payload.get("speed", 0),
                timestamp=datetime.fromisoformat(timestamp) if timestamp else None,
            )
            db = SessionLocal()
            try:
                create_gps_point(db, gps_payload)
            finally:
                db.close()
        except Exception as exc:
            print(f"MQTT GPS message ignored: {exc}")

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.mqtt_host, settings.mqtt_port, keepalive=60)

    thread = threading.Thread(target=client.loop_forever, daemon=True)
    thread.start()

