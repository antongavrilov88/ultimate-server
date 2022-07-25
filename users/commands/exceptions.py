from typing import Optional

from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from commands.exceptions import CreateFailedError, CommandInvalidError, CommandException, ObjectNotFoundError


class UsersEmailExistsValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("Must be unique")], field_name="email")


class UserPasswordValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("Wrong password")], field_name="password")


# class UserNotFoundError(ValidationError):
#     def __init__(self) -> None:
#         super().__init__([_("User not found")], field_name="email")


class UserAlreadyLoggedInError(ValidationError):
    def __init__(self) -> None:
        super().__init__([_("User already logged in")], field_name="email")


class UserCreateFailedError(CreateFailedError):
    message = "User couldn't be created"


class UserTokenFailedError(CommandInvalidError):
    message = "User couldn't be logged in"


class UserAuthorizationError(CommandInvalidError):
    message = "Unauthorized"


class UserInvalidError(CommandInvalidError):
    message = "User parameters are invalid."


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


class UserNotFoundError(ObjectNotFoundError):
    def __init__(self, user_id: Optional[str] = None,
                 exception: Optional[Exception] = None) -> None:
        super().__init__("User", user_id, exception)
