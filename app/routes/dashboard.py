from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime, timedelta
from app.extensions import mongo

from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)

# bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp .route('/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_id = user["_id"]

    # Fetch all detections for this user
    detections = list(mongo.db.detections.find({"user_id": user_id}))

    # --- Helmet Chart ---
    helmet_counts = {"Helmet": 0, "No Helmet": 0, "None": 0}
    for d in detections:
        helmet = d.get("helmet", "None")
        if helmet in helmet_counts:
            helmet_counts[helmet] += 1
        else:
            helmet_counts["None"] += 1

    # --- Zone Distribution ---
    zone_counts = {}
    for d in detections:
        zone = d.get("zone", "Unknown")
        zone_counts[zone] = zone_counts.get(zone, 0) + 1

    # --- Event Chart ---
    event_counts = {"Entered": 0, "Exited": 0, "Unattended": 0}
    for d in detections:
        event = d.get("event", "Unattended")
        if event in event_counts:
            event_counts[event] += 1
        else:
            event_counts["Unattended"] += 1

    # --- Recent Logs ---
    recent_logs = mongo.db.detections.find({"user_id": user_id}).sort("timestamp", -1).limit(10)
    recent_logs_list = [
        {
            "zone": log.get("zone", "-"),
            "event": log.get("event", "-"),
            "helmet": log.get("helmet", "-"),
            "face_id": log.get("face_id", "-"),
            "timestamp": log.get("timestamp").strftime("%Y-%m-%d %H:%M:%S") if log.get("timestamp") else "-"
        }
        for log in recent_logs
    ]

    return jsonify({
        "helmetChart": helmet_counts,
        "zoneDistribution": zone_counts,
        "eventChart": event_counts,
        "recentLogs": recent_logs_list
    })
