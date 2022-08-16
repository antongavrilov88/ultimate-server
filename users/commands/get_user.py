from commands.base import BaseCommand
from dao.exceptions import DAOGetFailedError
from models.user import User
from users.commands.exceptions import GetUserError, \
     UserDoesNotExistenceError, UnknownUserRequestError
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
        except Exception:
            raise UnknownUserRequestError()
        return user

    def validate(self) -> None:
        user_id = self._user_id

        user = UserDAO.find_by_id(user_id)
        if not user:
            raise UserDoesNotExistenceError()

