from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.extensions import mongo

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    mongo.db.users.insert_one({
        "username": username,
        "password": hashed_pw
    })

    return jsonify({"message": "Registration successful"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
    # access_token = create_access_token(
    # identity=str(user["_id"]),   # store _id as string
    # expires_delta=timedelta(days=1)
    # )   
    return jsonify({"token": access_token}), 200


# --------------------- Profile Routes ---------------------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    username = get_jwt_identity()
    
    # Fetch user and include _id, exclude password
    user = mongo.db.users.find_one({"username": username}, {"password": 0})
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Convert ObjectId to string for JSON serialization
    user["_id"] = str(user["_id"])

    return jsonify(user), 200



@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    new_username = data.get("username")
    new_password = data.get("password")

    update_data = {}
    if new_username and new_username != username:
        if mongo.db.users.find_one({"username": new_username}):
            return jsonify({"error": "Username already taken"}), 400
        update_data["username"] = new_username

    if new_password:
        update_data["password"] = generate_password_hash(new_password)

    if not update_data:
        return jsonify({"message": "Nothing to update"}), 400

    mongo.db.users.update_one({"username": username}, {"$set": update_data})

    return jsonify({"message": "Profile updated successfully"}), 200


@auth_bp.route("/profile", methods=["DELETE"])
@jwt_required()
def delete_profile():
    username = get_jwt_identity()
    result = mongo.db.users.delete_one({"username": username})
    
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    # Optionally delete related user data (e.g., zones)
    mongo.db.zones.delete_many({"user_id": result["_id"]})

    return jsonify({"message": "User account deleted"}), 200
