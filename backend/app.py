from flask import Flask
from flask_cors import CORS
from extensions import db, jwt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)
jwt.init_app(app)
CORS(app)


with app.app_context():
    db.create_all()

from routes import *


if __name__ == '__main__':
    app.run(debug=True)
