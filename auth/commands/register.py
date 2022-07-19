from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import jwt

from api.Exeptions import ValidationError
from auth.dao import TokenDAO
from config import BaseConfig
from dao.exceptions import DAOCreateFailedError
from models.user import User
from users.commands.exceptions import UserCreateFailedError, UserInvalidError, \
    UsersEmailExistsValidationError
from users.dao import UserDAO
from commands.base import BaseCommand
from werkzeug.security import generate_password_hash


class RegisterUserCommand(BaseCommand):
    def __init__(self, data: Dict[str, Any]):
        self._properties = data.copy()
        self._data = data.copy()
        self._token_data = {}

    def run(self) -> User:
        self.validate()
        try:
            user = UserDAO.create(self._data, commit=True)
            # create access token using JWT
            token = jwt.encode({'email': self._properties['email'], 'exp': datetime.utcnow() + timedelta(minutes=30)}, BaseConfig.SECRET_KEY)
            self._token_data['token'] = token
            self._token_data['user_id'] = user.get_id()
            token_obj = TokenDAO.create(self._token_data, commit=True)
        except DAOCreateFailedError as exception:
            raise UserCreateFailedError() from exception
        return user, token_obj

    def validate(self) -> None:
        exceptions: List[ValidationError] = []
        email: Optional[str] = self._properties.get('email')
        password: Optional[str] = self._properties.get('password')

        if not UserDAO.validate_email_uniqueness(email):
            exceptions.append(UsersEmailExistsValidationError)

        hashed_password = generate_password_hash(password)
        self._data['password'] = hashed_password


        if exceptions:
            exception = UserInvalidError()
            exception.add_list(exceptions)
            raise exception



