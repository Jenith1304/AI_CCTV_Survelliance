from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import cloudinary.uploader
from datetime import datetime
from app.extensions import mongo
from detection import detect_image, detect_video
import uuid
from bson import ObjectId
media_bp = Blueprint("media", __name__)
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@media_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_media():
    username = get_jwt_identity()
    # Fetch full user from DB
    user = mongo.db.users.find_one({"username": username})  # Or use email if that's the identity
    # Get the user's ObjectId
    user_id = user["_id"]
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    file_type = file.content_type

    if not (file_type.startswith("image/") or file_type.startswith("video/")):
        return jsonify({"error": "Only images or videos allowed"}), 400

    # Save uploaded file temporarily
    temp_filename = f"{uuid.uuid4().hex}_{file.filename}"
    local_path = os.path.join("temp_uploads", temp_filename)
    os.makedirs("temp_uploads", exist_ok=True)
    file.save(local_path)

    try:
        if file_type.startswith("image/"):
            processed_path = detect_image(local_path, user=user_id)  # this saves processed image with red boxes

            # Upload processed image (with red boxes) to Cloudinary
            cloudinary_result = cloudinary.uploader.upload(
                processed_path,
                folder="helmet_detection_uploads",
                resource_type="image"
            )

            file_url = cloudinary_result['secure_url']
            public_id = cloudinary_result['public_id']

            media_type = "image"

        elif file_type.startswith("video/"):
            # process and convert to MP4 (you must define detect_video properly)
            processed_filename = detect_video(local_path, user=user)
            processed_path = os.path.join("static", processed_filename)

            cloudinary_result = cloudinary.uploader.upload(
                processed_path,
                folder="helmet_detection_uploads",
                resource_type="video"
            )

            file_url = cloudinary_result['secure_url']
            public_id = cloudinary_result['public_id']
            media_type = "video"

        else:
            return jsonify({"error": "Unsupported file type"}), 400

    except Exception as e:
        return jsonify({"error": f"Processing or upload failed: {str(e)}"}), 500

    # Insert analysis result
    mongo.db.media.insert_one({
         "user_id": ObjectId(user_id),
        "file_url": file_url,
        "public_id": public_id,
        "media_type": media_type,
        "analysis": {
            "helmet_violation": True,
            "timestamp": datetime.utcnow()
        }
    })

    # Clean up local files
    os.remove(local_path)
    if os.path.exists(processed_path):
        os.remove(processed_path)

    return jsonify({"message": "Uploaded & analyzed successfully", "url": file_url}), 201

@media_bp.route("/uploads", methods=["GET"])
@jwt_required()
def get_user_uploads():
    username = get_jwt_identity()
    user = mongo.db.users.find_one({"username": username})
    user_id = user["_id"]

    uploads = list(mongo.db.media.find({"user_id": user_id}, {"_id": 0}))
    return jsonify(uploads), 200