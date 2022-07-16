from __future__ import annotations

from flask_appbuilder import Model

from sqlalchemy import (
    Column,
    Integer,
    String,
)


class User(Model):
    """The user object"""

    __table_name__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'User<{self.id}>'


