from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import jwt

from api.Exeptions import ValidationError
from auth.commands.exceptions import UnknownAuthError
from auth.dao import TokenDAO
from config import BaseConfig
from dao.exceptions import DAOCreateFailedError
from models.user import User
from users.commands.exceptions import UserCreateFailedError, UserInvalidError, \
    UsersEmailExistsValidationError, EmailConflictError
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
            user = UserDAO.create(self._data['data']['attributes'], commit=True)
            # create access token using JWT
            token = jwt.encode({'email': self._properties['data']['attributes']['email'], 'exp': datetime.utcnow() + timedelta(minutes=30)},
                               BaseConfig.SECRET_KEY)
            self._token_data['token'] = token
            self._token_data['user_id'] = user.get_id()
            self._token_data['jwt_token_active'] = True
            token_obj = TokenDAO.create(self._token_data, commit=True)
        except DAOCreateFailedError as exception:
            raise UserCreateFailedError() from exception
        except Exception:
            raise UnknownAuthError()
        return user, token_obj

    def validate(self) -> None:
        # exceptions: List[ValidationError] = []
        email: Optional[str] = self._properties.get('data').get('attributes').get('email')
        password: Optional[str] = self._properties.get('data').get('attributes').get('password')

        if not UserDAO.validate_email_uniqueness(email):
            raise EmailConflictError()

        # if exceptions:
        #     exception = EmailConflictError()
        #     exception.add_list(exceptions)
        #     raise exception

        hashed_password = generate_password_hash(password)
        self._data['data']['attributes']['password'] = hashed_password

        users_list = UserDAO.find_all()
        self._data['data']['attributes']['is_admin'] = len(users_list) == 0
