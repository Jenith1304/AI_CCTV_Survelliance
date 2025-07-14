# main.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
from extensions import mongo, jwt

# --- Load Environment Variables ---
# load_dotenv(os.path.join(os.path.dirname(__file__), 'app', '.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# load_dotenv()  # It will load from app/.env if run from app/

# --- Initialize Flask App ---

app = Flask(__name__, static_folder="static")



CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "https://ai-cctv-survelliance.onrender.com",
            "http://localhost:5000", 
            "http://127.0.0.1:5000",
        ]
    }
}, supports_credentials=True)

# --- Extensions & Config ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# mongo = PyMongo()
# jwt = JWTManager()

mongo.init_app(app)
jwt.init_app(app)
# --- Configure Cloudinary ---
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_API_KEY'),
    api_secret=os.getenv('CLOUD_API_SECRET')
)

# --- Register Blueprints ---
from routes.auth import auth_bp
from routes.zones import zones_bp
from routes.media import media_bp
from routes.stream import stream_bp
from app.routes.email_config import email_bp
from app.routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(zones_bp, url_prefix="/api")
app.register_blueprint(media_bp, url_prefix="/api/media")
app.register_blueprint(stream_bp, url_prefix="/api/stream")
app.register_blueprint(email_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

# --- Serve Frontend ---
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
