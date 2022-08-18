from typing import Optional
from flask_babel import gettext as _

from exceptions import UltimateServerException


class CommandException(UltimateServerException):
    """ Common base class for Command exceptions. """

    def __repr__(self) -> str:
        if self._exception:
            return repr(self._exception)
        return repr(self)


class ObjectAlreadyExistsError(CommandException):
    status = 409
    message_format = "{} {} already exists."

    def __init__(
            self,
            object_type: str,
            object_id: Optional[str] = None,
            exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(
            _(
                self.message_format.format(
                    object_type, '"%s" ' % object_id if object_id else ""
                )
            ),
            exception,
        )


class ObjectNotFoundError(CommandException):
    status = 404
    message_format = "{} {}not found."

    def __init__(
            self,
            object_type: str,
            object_id: Optional[str] = None,
            exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(
            self.message_format.format(
                    object_type, '"%s" ' % object_id if object_id else ""
                )
            ,
            exception,
        )


class CreateFailedError(CommandException):
    status = 500
    message = "Command create failed"


class CommandInvalidError(CommandException):
    """ Common base class for Command Invalid errors. """

    status = 422

    def __init__(self, message: str = "") -> None:
        super().__init__(message)
