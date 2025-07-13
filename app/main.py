
# main.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
from flask_cors import CORS 
from flask import send_from_directory

# --- Load Environment Variables ---
load_dotenv(os.path.join(os.path.dirname(__file__), 'app', '.env'))

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists("app/static/" + path):
        return send_from_directory("app/static", path)
    else:
        return send_from_directory("app/static", "index.html")
# --- Import Blueprints ---
from routes.auth import auth_bp
from routes.zones import zones_bp
from routes.media import media_bp
from routes.stream import stream_bp
from app.extensions import mongo, jwt
from app.routes.email_config import email_bp
from app.routes.dashboard import dashboard_bp
from flask_jwt_extended import JWTManager   


# --- Configuration ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# --- Initialize Extensions ---

mongo.init_app(app)
jwt.init_app(app)
# --- Configure Cloudinary ---
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_API_KEY'),
    api_secret=os.getenv('CLOUD_API_SECRET')
)


# --- Register Blueprints ---
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(zones_bp, url_prefix="/api")
app.register_blueprint(media_bp, url_prefix="/api/media")
app.register_blueprint(stream_bp, url_prefix="/api/stream")
app.register_blueprint(email_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

# --- Main ---
if __name__ == "__main__":
    app.run(debug=True)

