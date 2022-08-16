from typing import Optional

from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from commands.exceptions import CreateFailedError, CommandInvalidError, CommandException, ObjectNotFoundError


class UsersEmailExistsValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__(["Must be unique"], field_name="email")


class UserPasswordValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__(["Wrong password"], field_name="password")


class UserDoesNotExistError(ValidationError):
    def __init__(self) -> None:
        super().__init__(["User not found"], field_name="email")


class UserCreateFailedError(CreateFailedError):
    message = "User couldn't be created"


class UserTokenFailedError(CommandInvalidError):
    message = "User couldn't be logged in"


class UserAuthorizationError(CommandInvalidError):
    message = "Unauthorized"


class UserInvalidError(CommandInvalidError):
    message = "User parameters are invalid."


class EmailConflictError(CommandInvalidError):
    message = "Email already taken."


class UserDoesNotExistenceError(CommandInvalidError):
    message = "User not found."


class UsersListLimitAccessError(CommandInvalidError):
    message = "Forbidden."


class GetUsersListError(CommandInvalidError):
    message = "Processing error."


class GetUsersListError(CommandInvalidError):
    message = "Processing error."


class GetUserError(CommandInvalidError):
    message = "Processing error."


class AccessDeniedError(CommandInvalidError):
    message = "Access denied"


class UserNotFoundError(CommandInvalidError):
    message = "User not found."


class UnknownUserRequestError(CommandInvalidError):
    message = "Unknown internal server error."


class WrongPasswordValidationError(CommandInvalidError):
    message = "Wrong password."
