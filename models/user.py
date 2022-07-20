from __future__ import annotations


from flask_appbuilder import Model

from sqlalchemy import (
    Column,
    Integer,
    String, Boolean,
)
from sqlalchemy.sql.elements import BinaryExpression


class User(Model):
    """The user object"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean())

    def __repr__(self) -> str:
        return f'User<{self.id}>'

    @classmethod
    def get_by_email(cls, email) -> User:
        from api import db
        session = db.session()
        qry = session.query(User).filter(email_filter(email))
        return qry.one_or_none()

    def get_id(self):
        return self.id

def email_filter(email: str) -> BinaryExpression:
    return User.email == email
