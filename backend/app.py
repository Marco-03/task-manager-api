# app.py
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Use SQLite file in /tmp for CI testing to persist across requests
if os.getenv("TESTING") == "1":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)
jwt.init_app(app)
CORS(app, origins=["http://localhost:3000", "https://task-manager-api-lbva.onrender.com"])

# Ensure tables exist
with app.app_context():
    if os.getenv("TESTING") == "1":
        # Drop existing tables in CI to start fresh
        db.drop_all()
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
