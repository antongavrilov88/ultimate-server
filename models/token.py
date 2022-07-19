from __future__ import annotations

from flask_appbuilder import Model

from sqlalchemy import (
    Column,
    Integer,
    String, ForeignKey,
)


class Token(Model):
    """The token model"""

    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(256))
