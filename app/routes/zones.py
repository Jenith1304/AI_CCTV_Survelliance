from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId

zones_bp = Blueprint("zones", __name__)

@zones_bp.route("/zones", methods=["POST"])
@jwt_required()
def add_zone():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username}) 
    user_id = user["_id"]

    data = request.get_json()
    zone_name = data.get("zone_name")
    x1 = data.get("x1")
    y1 = data.get("y1")
    x2 = data.get("x2")
    y2 = data.get("y2")

    if not all([zone_name, x1, y1, x2, y2]):
        return jsonify({"error": "All fields are required"}), 400

    mongo.db.zones.insert_one({
        "user_id": ObjectId(user_id),
        "zone_name": zone_name,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2
    })

    return jsonify({"message": f"Zone '{zone_name}' added"}), 201

@zones_bp.route("/zones", methods=["GET"])
@jwt_required()
def get_zones():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    user_id = user["_id"]

    zones_cursor = mongo.db.zones.find({"user_id": user_id})
    zones = []
    for zone in zones_cursor:
        zones.append({
            "_id": str(zone["_id"]),
            "zone_name": zone.get("zone_name"),
            "x1": zone.get("x1"),
            "y1": zone.get("y1"),
            "x2": zone.get("x2"),
            "y2": zone.get("y2")
        })

    return jsonify(zones), 200
0


@zones_bp.route("/zones/<zone_id>", methods=["DELETE"])
@jwt_required()
def delete_zone(zone_id):
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    user_id = user["_id"]

    result = mongo.db.zones.delete_one({
        "_id": ObjectId(zone_id),
        "user_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        return jsonify({"error": "Zone not found or unauthorized"}), 404

    return jsonify({"message": "Zone deleted successfully"}), 200
