from __future__ import annotations

from typing import Any, Dict

from flask_appbuilder import Model

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.sql.elements import BinaryExpression



class User(Model):
    """The user object"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'User<{self.id}>'

    @classmethod
    def get_by_email(cls, email) -> User:
        from api import db
        session = db.session()
        qry = session.query(User).filter(email_filter(email))
        return qry.one_or_none()

    def get_data(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password
        }

def email_filter(email: str) -> BinaryExpression:
    return User.email == email



