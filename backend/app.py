from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from dotenv import load_dotenv
import os
from models import User, Task  # noqa: F401


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

# Use SQLite in /tmp for testing to persist across requests
if os.getenv("TESTING") == "1":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
jwt.init_app(app)
CORS(app, origins=["http://localhost:3000", "https://task-manager-api-lbva.onrender.com"])

with app.app_context():
    if os.getenv("TESTING") == "1":
        db.drop_all()  # ensure fresh start in CI
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
