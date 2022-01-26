import os
from dotenv import load_dotenv
from flask.app import Flask
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
mongo = PyMongo(app)
# Setup the Flask-JWT-Extended extension
app.config['SECRET_KEY'] = os.getenv('APP_SECRET')

import backend.routes.index
import backend.routes.login