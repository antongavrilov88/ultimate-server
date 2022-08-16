from marshmallow import ValidationError

from commands.exceptions import CommandInvalidError


class TokenNotFoundError(ValidationError):
    def __init__(self) -> None:
        super().__init__(["Token not found"], field_name="token")


class TokenInvalidError(CommandInvalidError):
    message = "Token parameters are invalid."


class UserTokenFailedError(CommandInvalidError):
    message = "User couldn't be logged out"


class UnknownAuthError(CommandInvalidError):
    message = "Unknown internal server error"
