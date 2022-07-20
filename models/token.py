from __future__ import annotations

from flask_appbuilder import Model

from sqlalchemy import (
    Column,
    Integer,
    String, ForeignKey, Boolean,
)


class Token(Model):
    """The token model"""

    __tablename__ = "tokens"
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey("users.id"), nullable=False)
    token = Column(String(256))
    jwt_token_active = Column(Boolean())

    def set_jwt_token_active(self):
        self.jwt_token_active = True

    def set_jwt_token_inactive(self):
        self.jwt_token_active = False

    def get_is_token_active_status(self):
        self.jwt_token_active
