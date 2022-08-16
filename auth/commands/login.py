from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import jwt

from api.Exeptions import ValidationError
from auth.commands.exceptions import UnknownAuthError
from auth.dao import TokenDAO
from commands.base import BaseCommand
from config import BaseConfig
from dao.exceptions import DAOCreateFailedError
from users.commands.exceptions import UserNotFoundError, UserPasswordValidationError, \
    UserTokenFailedError, WrongPasswordValidationError
from users.dao import UserDAO
from werkzeug.security import check_password_hash


class LoginUserCommand(BaseCommand):
    def __init__(self, data: Dict[str, Any]):
        self._user = None
        self._properties = data.copy()
        self._token_data = {}

    def run(self) -> Any:
        self.validate()
        try:
            token = TokenDAO.create(self._token_data, commit=True)
        except DAOCreateFailedError as exception:
            raise UserTokenFailedError() from exception
        except Exception:
            raise UnknownAuthError()
        return self._user, token

    def validate(self) -> None:
        email: Optional[str] = self._properties.get('data').get('attributes').get('email')
        password: Optional[str] = self._properties.get('data').get('attributes').get('password')
        
        user = UserDAO.get_by_email(email)

        if not user:
            raise UserNotFoundError()
        if user:
            self._user = user
            if not check_password_hash(user.password, password):
                raise WrongPasswordValidationError()
            if check_password_hash(user.password, password):

                token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                                   BaseConfig.SECRET_KEY)
                self._token_data['token'] = token
                self._token_data['user_id'] = user.get_id()
                self._token_data['jwt_token_active'] = True

