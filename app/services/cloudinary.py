import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

def upload_to_cloudinary(file_path, resource_type='image'):
    try:
        response = cloudinary.uploader.upload(file_path, resource_type=resource_type)
        return response.get("secure_url")
    except Exception as e:
        print("[CLOUDINARY ERROR]", e)
        return None
