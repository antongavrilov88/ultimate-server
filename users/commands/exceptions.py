from typing import Optional
from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from commands.exceptions import ObjectNotFoundError, CreateFailedError, CommandInvalidError


class UsersEmailExistsValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("Must be unique")], field_name="email")


class UserPasswordValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("Wrong password")], field_name="password")


class UserNotFoundError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("User not found")], field_name="email")


class UserAlreadyLoggedInError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("User already logged in")], field_name="email")


class UserCreateFailedError(CreateFailedError):
    message = "User couldn't be created"


class UserTokenFailedError(CommandInvalidError):
    message = "User couldn't be logged in"


class UserInvalidError(CommandInvalidError):
    message = "User parameters are invalid."
