from enum import Enum
import typing
from flask import make_response, jsonify
from config import api_version_str


class APIError(Enum):
    UNKNOWN_EXCEPTION = 1
    NOT_JSON = 2
    WRONG_API = 3


errors = {
    APIError.UNKNOWN_EXCEPTION: {'code': 'Exception', 'title': 'Request can not be done'},
    APIError.NOT_JSON: {'code': 'DataNotJSON', 'title': 'Data has not JSON format'},
    APIError.WRONG_API: {'code': 'WrongAPI', 'title': 'Wrong API'}
}


def default_response_object():
    return {
        'jsonapi': {
            'version': api_version_str
        },
        'meta': {
            'copyright': 'AGwallet server',
            'authors': [
                'Anton Gavrilov'
            ]
        }
    }


def error_response_object(code, title):
    response_object = default_response_object()
    response_object['errors'] = [{
        'code': code,
        'title': title
    }]
    return response_object


def make_success_response(response_object, code: int):
    return make_response(jsonify(response_object)), code


def make_error_response(error: APIError, code: int):
    response_object = error_response_object(errors[error]['code'], errors[error]['title'])
    return make_response(jsonify(response_object)), code


def make_bad_request_response(error: APIError):
    return make_error_response(error, 400)


def make_unauthorized_response(error: APIError):
    return make_error_response(error, 401)


def make_forbidden_response(error: APIError):
    return make_error_response(error, 403)


def make_not_found_response(error: APIError):
    return make_error_response(error, 404)


def make_conflict_response(error: APIError):
    return make_error_response(error, 409)


def make_internal_server_error_response(error: APIError):
    return make_error_response(error, 500)


SCHEMA = "_schema"


class MarshmallowError(Exception):
    """Base class for all marshmallow-related errors."""


class ValidationError(MarshmallowError):
    """Raised when validation fails on a field or schema.

    Validators and custom fields should raise this exception.

    :param message: An error message, list of error messages, or dict of
        error messages. If a dict, the keys are subitems and the values are error messages.
    :param field_name: Field name to store the error on.
        If `None`, the error is stored as schema-level error.
    :param data: Raw input data.
    :param valid_data: Valid (de)serialized data.
    """

    def __init__(
            self,
            message: typing.Union[str, typing.List, typing.Dict],
            field_name: str = SCHEMA,
            data: typing.Optional[
                typing.Union[
                    typing.Mapping[str, typing.Any],
                    typing.Iterable[typing.Mapping[str, typing.Any]],
                ]
            ] = None,
            valid_data: typing.Optional[
                typing.Union[
                    typing.List[typing.Dict[str, typing.Any]],
                    typing.Dict[str, typing.Any],
                ]
            ] = None,
            **kwargs
    ):
        self.messages = [message] if isinstance(message, (str, bytes)) else message
        self.field_name = field_name
        self.data = data
        self.valid_data = valid_data
        self.kwargs = kwargs
        super().__init__(message)

    def normalized_messages(self):
        if self.field_name == SCHEMA and isinstance(self.messages, dict):
            return self.messages
        return {self.field_name: self.messages}
