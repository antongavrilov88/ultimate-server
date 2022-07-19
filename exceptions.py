from typing import Optional, Dict, Any

from errors import UltimateServerErrorType


class UltimateServerException(Exception):
    status = 500
    message = ""

    def __init__(
        self,
        message: str = "",
        exception: Optional[Exception] = None,
        error_type: Optional[UltimateServerErrorType] = None,
    ) -> None:
        if message:
            self.message = message
        self._exception = exception
        self._error_type = error_type
        super().__init__(self.message)

    @property
    def exception(self) -> Optional[Exception]:
        return self._exception

    @property
    def error_type(self) -> Optional[UltimateServerErrorType]:
        return self._error_type

    def to_dict(self) -> Dict[str, Any]:
        rv = {}
        if hasattr(self, "message"):
            rv["message"] = self.message
        if self.error_type:
            rv["error_type"] = self.error_type
        if self.exception is not None and hasattr(self.exception, "to_dict"):
            rv = {**rv, **self.exception.to_dict()}  # type: ignore
        return rv