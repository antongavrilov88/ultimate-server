from typing import List

from flask import make_response

from api.Exeptions import ValidationError
from commands.base import BaseCommand
from commands.exceptions import CommandInvalidError
from dao.exceptions import DAOGetFailedError
from models.user import User
from users.commands.exceptions import UsersListLimitAccessError, GetUsersListError, AccessDeniedError
from users.dao import UserDAO


class GetUsersListCommand(BaseCommand):
    def __init__(self, user: User, token: str):
        self._token = token
        self._user = user

    def run(self) -> List[User]:
        self.validate()
        try:
            users_list = UserDAO.find_all()
        except DAOGetFailedError as exception:
            raise GetUsersListError from exception
        return users_list

    def validate(self) -> None:
        exceptions: List[ValidationError] = []

        if exceptions:
            exception = GetUsersListError()
            exception.add_list(exceptions)
            raise exception
