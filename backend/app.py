# app.py
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt  # importă din extensions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
jwt.init_app(app)
CORS(app)

# Import modelul după ce ai configurat `db`
from models import User

with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return {"msg": "Backend is running"}

from routes import *


if __name__ == '__main__':
    app.run(debug=True)
