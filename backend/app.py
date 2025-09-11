# app.py
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Use in-memory DB for testing in CI if TESTING env var is set
if os.getenv("TESTING") == "1":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)
jwt.init_app(app)
CORS(app, origins=["http://localhost:3000", "https://task-manager-api-lbva.onrender.com"])

with app.app_context():
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
