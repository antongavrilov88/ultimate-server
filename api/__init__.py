import json

from flask import Flask
from flask_appbuilder import SQLA
from flask_cors import CORS
from .routes import api

"""Init database"""
db = SQLA()

"""Init app"""
app = Flask(__name__)

api.init_app(app)

app.config.from_object('api.config.BaseConfig')

CORS(app)


@app.after_request
def after_request(response):
    """
       Sends back a custom error with {"success", "msg"} format
    """

    if int(response.status_code) >= 400:
        response_data = json.loads(response.get_data())
        if "errors" in response_data:
            response_data = {"success": False,
                             "msg": list(response_data["errors"].items())[0][1]}
            response.set_data(json.dumps(response_data))
        response.headers.add('Content-Type', 'application/json')
    return response
