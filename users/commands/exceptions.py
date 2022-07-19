from typing import Optional
from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from commands.exceptions import ObjectNotFoundError, CreateFailedError, CommandInvalidError


class UsersEmailExistsValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("Must be unique")], field_name="email")


class UserNotFoundError(ObjectNotFoundError):
    def __init__(
            self, user_id: Optional[str] = None, exception: Optional[Exception] = None
    ) -> None:
        super().__init__("User", user_id, exception)


class UserCreateFailedError(CreateFailedError):
    message = "User couldn't be created"


class UserInvalidError(CommandInvalidError):
    message = "User parameters are invalid."
