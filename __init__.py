from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

# app = Flask(__name__)
# db = SQLAlchemy()
# app.config['CORS_HEADERS'] = 'Content-Type'

# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/postgres'


app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@irsdb:5432/postgres'
db.init_app(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://0.0.0.0"}})


try:
    with app.app_context():
        db.engine.connect()
        print("Database connection successful!")
except Exception as e:
    print("Oh no! Database connection failed:", e)

