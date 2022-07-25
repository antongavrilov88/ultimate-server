from typing import Optional, Dict, Any, List
from flask_babel import gettext as _

from api.Exeptions import ValidationError
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
        self._invalid_exceptions: List[ValidationError] = []
        super().__init__(message)

    def add(self, exception: ValidationError) -> None:
        self._invalid_exceptions.append(exception)

    def add_list(self, exceptions: List[ValidationError]) -> None:
        self._invalid_exceptions.extend(exceptions)

    def normalized_messages(self) -> Dict[Any, Any]:
        errors: Dict[Any, Any] = {}
        for exception in self._invalid_exceptions:
            errors.update(exception.normalized_messages())
        return errors
