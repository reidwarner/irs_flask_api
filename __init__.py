from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
db = SQLAlchemy()
CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db.init_app(app)