from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import jwt

from api.Exeptions import ValidationError
from auth.dao import TokenDAO
from commands.base import BaseCommand
from config import BaseConfig
from dao.exceptions import DAOCreateFailedError
from users.commands.exceptions import UserNotFoundError, UserPasswordValidationError, \
    UserTokenFailedError
from users.dao import UserDAO
from werkzeug.security import check_password_hash


class LoginUserCommand(BaseCommand):
    def __init__(self, data: Dict[str, Any]):
        self._properties = data.copy()
        self._token_data = {}

    def run(self) -> Any:
        self.validate()
        try:
            login_response = TokenDAO.create(self._token_data, commit=True)
        except DAOCreateFailedError as exception:
            raise UserTokenFailedError() from exception
        return login_response

    def validate(self) -> None:
        exceptions: List[ValidationError] = []
        email: Optional[str] = self._properties.get('email')
        password: Optional[str] = self._properties.get('password')
        user = UserDAO.get_by_email(email)

        if not user:
            exceptions.append(UserNotFoundError)
        if user:
            if not check_password_hash(user.password, password):
                exceptions.append(UserPasswordValidationError)
            if check_password_hash(user.password, password):

                token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                                   BaseConfig.SECRET_KEY)
                self._token_data['token'] = token
                self._token_data['user_id'] = user.get_id()
                self._token_data['jwt_token_active'] = True

        if exceptions:
            exception = UserTokenFailedError()
            exception.add_list(exceptions)
            raise exception
