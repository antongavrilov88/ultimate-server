from dao.base import BaseDAO
from models.token import Token
from models.user import User


class TokenDAO(BaseDAO):
    model_cls = Token

    @staticmethod
    def get_by_value(token: str) -> Token:
        from api import db
        token_query = db.session.query(Token).filter(Token.token == token)
        token = token_query.one_or_none()
        return token
