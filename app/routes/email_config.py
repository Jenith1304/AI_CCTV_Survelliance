from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import mongo
from bson import ObjectId

email_bp = Blueprint("email", __name__)

@email_bp.route("/email-config", methods=["POST"])
@jwt_required()
def set_email_config():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    user_id = user["_id"]

    existing = mongo.db.email_config.find_one({"user_id": user_id})
    if existing:
        return jsonify({"error": "Email config already exists. Delete it before adding a new one."}), 400

    data = request.get_json()
    sender = data.get("sender")
    app_password = data.get("app_password")
    receiver = data.get("receiver")

    if not all([sender, app_password, receiver]):
        return jsonify({"error": "All fields are required"}), 400

    mongo.db.email_config.insert_one({
        "user_id": user_id,
        "sender": sender,
        "app_password": app_password,
        "receiver": receiver
    })

    return jsonify({"message": "Email configuration saved successfully."}), 200

@email_bp.route("/email-config", methods=["GET"])
@jwt_required()
def get_email_config():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    user_id = user["_id"]

    config = mongo.db.email_config.find_one({"user_id": user_id}, {"_id": 0})
    if not config:
        return jsonify({})
    return jsonify(config), 200

@email_bp.route("/email-config", methods=["DELETE"])
@jwt_required()
def delete_email_config():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    user_id = user["_id"]

    result = mongo.db.email_config.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        return jsonify({"error": "No email config found to delete"}), 404

    return jsonify({"message": "Email config deleted"}), 200
