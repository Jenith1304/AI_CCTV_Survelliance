# app/__init__.py
# app/__init__.py

from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask import Flask
mongo = PyMongo()
jwt = JWTManager()
# app = Flask(__name__, static_folder="static", static_url_path="/")