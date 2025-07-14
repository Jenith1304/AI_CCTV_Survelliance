# mongo.py (or better, inside detection.py directly if already imported)
from datetime import datetime
from extensions import mongo  # make sure you're importing this correctly

def log_event(user_id, zone_name, face_id, helmet_status, event_type):
    try:
        print(f"[LOGGED] {event_type} | {zone_name} | {face_id} | {helmet_status}")
        mongo.db.detections.insert_one({
            "user_id": user_id,
            "zone": zone_name,
            "face_id": face_id,
            "helmet": helmet_status,
            "event": event_type,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        print(f"[ERROR] Failed to log detection: {e}")
