from typing import Any, Dict, List

from api.Exeptions import ValidationError
from auth.commands.exceptions import TokenNotFoundError, TokenInvalidError, UserTokenFailedError, UnknownAuthError
from auth.dao import TokenDAO
from commands.base import BaseCommand
from dao.exceptions import DAOCreateFailedError


class LogoutUserCommand(BaseCommand):
    def __init__(self, token: str):
        self._token_obj = None
        self._token = token

    def run(self) -> Any:
        self.validate()
        try:
            TokenDAO.update(self._token_obj, {"jwt_token_active": False}, commit=True)
        except DAOCreateFailedError as exception:
            raise UserTokenFailedError() from exception
        except Exception:
            raise UnknownAuthError()
        return {"logout_status": "success"}

    def validate(self) -> None:
        token = self._token

        token_obj = TokenDAO.get_by_value(token)

        if not token_obj:
            raise TokenInvalidError()

        self._token_obj = token_obj


