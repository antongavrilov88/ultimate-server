from users.commands.exceptions import UserNotFoundError
from dao.base import BaseDAO
from models.user import User


class UserDAO(BaseDAO):
    model_cls = User

    @staticmethod
    def get_by_email(email: str) -> User:
        user = User.get(email)
        if not user:
            raise UserNotFoundError()
        return user

    @staticmethod
    def validate_email_uniqueness(email: str) -> bool:
        if not email:
            return True
        from api import db
        user_query = db.session.query(User).filter(User.email == email)
        return not db.session.query(user_query.exists()).scalar()


