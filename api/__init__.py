import json

from flask import Flask, Blueprint
from flask_appbuilder import SQLA
from flask_cors import CORS

import api.config
from .routes import rest_api

db = SQLA()

app = Flask(__name__)

app.config.from_object(api.config.BaseConfig)

blueprint = Blueprint('api', __name__, url_prefix='/api')
rest_api.init_app(app)

CORS(app)

