from datetime import datetime
from functools import wraps

import jwt
from flask import request, make_response

from auth.dao import TokenDAO
from config import BaseConfig
from users.dao import UserDAO


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "authorization" in request.headers:
            token = request.headers["authorization"]
        if not token:
            return make_response({'message': 'Unauthorized'}, 401)

        token_data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
        token_obj = TokenDAO.get_by_value(token)
        current_user = UserDAO.get_by_email(token_data["email"])

        if not current_user:
            return make_response({'message': 'User not found'}, 404)

        if not token_obj.jwt_token_active:
            return make_response({"message": "Token is blocked"}, 401)

        expiration_time = datetime.utcfromtimestamp(token_data["exp"])
        now = datetime.utcnow()

        is_token_expired = now < expiration_time

        if is_token_expired:
            token_obj.set_jwt_token_inactive()
            TokenDAO.save(token_obj)
        return f(*args, **kwargs, current_user=current_user)

    return decorator
