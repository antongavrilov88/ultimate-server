from dao.base import BaseDAO
from models.token import Token
from models.user import User


class TokenDAO(BaseDAO):
    model_cls = Token

    @staticmethod
    def get_by_email(user: User) -> Token:
        from api import db
        token_query = db.session.query(Token).filter(Token.user_id == user.id)
        token = token_query.one_or_none()
        return token
