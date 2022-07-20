import json
from datetime import datetime, timedelta

import jwt
from flask import Flask, request, make_response
from flask_appbuilder import SQLA
from flask_cors import CORS

from auth.dao import TokenDAO
from config import BaseConfig
from models.user import User
from utils.token_required import token_required
from .routes import api

"""Init database"""
db = SQLA()

"""Init app"""
app = Flask(__name__)

db.init_app(app)
api.init_app(app)

app.config.from_object('api.config.BaseConfig')

CORS(app)


# @app.before_request(f)
# def check_token(f, check=False):
#     print(321, f)
#     if not check:
#         return
#     token = None
#     if "authorization" in request.headers:
#         token = request.headers["authorization"]
#     if not token:
#         return make_response({'message': 'Unauthorized'}, 401)
#     token_data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
#     token_obj = TokenDAO.get_by_email(token_data["email"])
#     current_user = User.get_by_email(token_data["email"])
#     if not current_user:
#         return make_response({'message': 'User not found'}, 404)
#     is_token_expired = token_data["exp"] - datetime.utcnow() > timedelta(minutes=30)
#     if is_token_expired:
#         token_obj.set_jwt_token_inactive()
#         TokenDAO.save(token_obj)
#     if not token_obj.get_is_token_active_status():
#         return make_response({"message": "Token is blocked"}, 401)

