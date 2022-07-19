import json

from flask import Flask
from flask_appbuilder import SQLA
from flask_cors import CORS
from .routes import api

"""Init database"""
db = SQLA()

"""Init app"""
app = Flask(__name__)

db.init_app(app)
api.init_app(app)

app.config.from_object('api.config.BaseConfig')

CORS(app)
