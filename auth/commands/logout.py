from typing import Any, Dict, List

from api.Exeptions import ValidationError
from auth.commands.exceptions import TokenNotFoundError, TokenInvalidError, UserTokenFailedError
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
        return {"logout_status": "success"}

    def validate(self) -> None:
        exceptions: List[ValidationError] = []
        token = self._token

        token_obj = TokenDAO.get_by_value(token)

        if not token_obj:
            exceptions.append(TokenNotFoundError)

        self._token_obj = token_obj

        if exceptions:
            exception = TokenInvalidError()
            exception.add_list(exceptions)
            raise exception
