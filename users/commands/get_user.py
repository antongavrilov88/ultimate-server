from typing import List

from api.Exeptions import ValidationError
from commands.base import BaseCommand
from dao.exceptions import DAOGetFailedError
from models.user import User
from users.commands.exceptions import GetUserError, UserNotFoundError
from users.dao import UserDAO


class GetUserCommand(BaseCommand):
    def __init__(self, user_id):
        self._user_id = user_id

    def run(self) -> User:
        self.validate()
        try:
            user = UserDAO.find_by_id(self._user_id)
        except DAOGetFailedError as exception:
            raise GetUserError from exception
        return user

    def validate(self) -> None:
        exceptions: List[ValidationError] = []
        user_id = self._user_id

        try:
            user = UserDAO.find_by_id(user_id)
            if not user:
                raise UserNotFoundError()
        except ValidationError as ex:
            exceptions.append(ex)

        if exceptions:
            exception = GetUserError()
            exception.add_list(exceptions)
            raise exception
