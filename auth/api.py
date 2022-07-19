from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields, abort, marshal

from api.Exeptions import make_bad_request_response, APIError, ValidationError
from api.UltimateServerResponseCreator import UltimateServerResponseCreator
from auth.commands.register import RegisterUserCommand
from commands.exceptions import CreateFailedError
from users.commands.exceptions import UsersEmailExistsValidationError, UserCreateFailedError, UserInvalidError

api = Namespace('auth', description='Authorization related operations')

register_request = api.model('register_request', {
    'email': fields.String(description='The task...'),
    'password': fields.String(description='The task...'),
})

register_data_content = api.model('register_data_content', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(readonly=True, description='The task...'),
    'password': fields.String(readonly=True, description='The task...'),
})

register_data = api.model('register_data', {
    'type': fields.String(default='auth'),
    'data': fields.Nested(register_data_content)
})

register_error = api.model('register_error', {
    'message': fields.String(readonly=True)
})


@api.errorhandler(UserInvalidError)
@api.marshal_with(register_error, code=409, description="Email already used")
def handle_email_conflict_exception(error):
    """This is an email conflict error"""
    return {'message': error.message}, 409


@api.errorhandler(CreateFailedError)
@api.marshal_with(register_error, code=500, description="User couldn't be created")
def handle_entity_processing_exception(error):
    """This is an unknown error"""
    return {'message': error.message}, 500


@api.errorhandler(Exception)
@api.marshal_with(register_error, code=500, description="Internal server error")
def handle_internal_server_exception(error):
    """This is an internal server error"""
    return {'message': error}, 500


@api.route('/register')
class AuthRestApi(Resource):
    """Register new user"""

    response_creator = UltimateServerResponseCreator('auth')

    @api.doc('register_user', responses={
        201: 'Success',
        400: 'Wrong API',
        409: 'Email conflict',
        500: 'Internal server'
    })
    @api.expect(register_request, validate=True)
    @api.marshal_with(register_data, code=201, description="User created")
    @api.marshal_with(register_error, code=400, description="Wrong API")
    @api.marshal_with(register_error, code=409, description="Email already registered")
    @api.marshal_with(register_error, code=500, description="User couldn't be created")
    def post(self):
        if not request.is_json:
            return make_bad_request_response(APIError.WRONG_API)
        new_user = RegisterUserCommand(request.json).run()
        return self.response_creator.response_201(new_user)
