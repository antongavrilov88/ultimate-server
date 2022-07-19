from typing import Dict, Any, List, Optional
from flask_appbuilder.models.sqla import Model

from api.Exeptions import ValidationError
from dao.exceptions import DAOCreateFailedError
from models.user import User
from users.commands.exceptions import UserCreateFailedError, UserInvalidError, \
    UsersEmailExistsValidationError
from users.dao import UserDAO
from commands.base import BaseCommand


class RegisterUserCommand(BaseCommand):
    def __init__(self, data: Dict[str, Any]):
        self._properties = data.copy()

    def run(self) -> User:
        self.validate()
        try:
            user = UserDAO.create(self._properties, commit=True)
        except DAOCreateFailedError as exception:
            raise UserCreateFailedError() from exception
        return user

    def validate(self) -> None:
        exceptions: List[ValidationError] = []
        email: Optional[str] = self._properties.get('email')

        if not UserDAO.validate_email_uniqueness(email):
            exceptions.append(UsersEmailExistsValidationError)

        if exceptions:
            exception = UserInvalidError()
            exception.add_list(exceptions)
            raise exception



