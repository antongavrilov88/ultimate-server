from flask import request
from flask_restx import Resource, Namespace, fields

from api.Exeptions import make_bad_request_response, APIError
from api.UltimateServerResponseCreator import UltimateServerResponseCreator
from auth.commands.exceptions import UnknownAuthError
from auth.commands.login import LoginUserCommand
from auth.commands.logout import LogoutUserCommand
from auth.commands.register import RegisterUserCommand
from commands.exceptions import CreateFailedError
from users.commands.exceptions import UserTokenFailedError, UsersEmailExistsValidationError, \
    UserPasswordValidationError, EmailConflictError, UserNotFoundError, WrongPasswordValidationError
from utils.token_required import token_required

api = Namespace('auth', description='Authorization related operations', sequrity='Bearer Auth')

register_attributes = api.model('register_attributes', {
    'email': fields.String(description='The task...'),
    'password': fields.String(description='The task...'),
})

login_attributes = api.model('login_attributes', {
    'email': fields.String(description='The task...'),
    'password': fields.String(description='The task...'),
})

register_response_attributes = api.model('register_response_attributes', {
    'email': fields.String(description='Users email'),
    'is_admin': fields.Boolean(description='Is user admin')
})

login_response_attributes = api.model('login_response_attributes', {
    'email': fields.String(description='Users email'),
    'is_admin': fields.Boolean(description='Is user admin')
})

auth_token_model = api.model('auth_token_model', {
    'token': fields.String(description='Access token')
})

auth_relationships = api.model('auth_relationships', {
    'token': fields.Nested(auth_token_model)
})

register_data_model = api.model('register_data_model', {
    'attributes': fields.Nested(register_attributes),
})

login_data_model = api.model('login_data_model', {
    'attributes': fields.Nested(login_attributes),
})

register_data_response_model = api.model('register_data_response_model', {
    'attributes': fields.Nested(register_response_attributes)
})

register_request = api.model('register_request', {
    'type': fields.String(description='The task...'),
    'data': fields.Nested(register_data_model),
})

register_data_content = api.model('register_data_content', {
    'id': fields.Integer(readonly=True),
    'attributes': fields.Nested(register_response_attributes),
    'relationships': fields.Nested(auth_relationships)
})

register_data = api.model('register_data', {
    'type': fields.String(default='auth'),
    'data': fields.Nested(register_data_content)
})

register_error: object = api.model('register_error', {
    'message': fields.String(readonly=True)
})

login_request = api.model('login_request', {
    'type': fields.String(description='The task...'),
    'data': fields.Nested(register_data_model),
})

login_data_content = api.model('login_data_content', {
    'id': fields.Integer(readonly=True),
    'attributes': fields.Nested(login_response_attributes),
    'relationships': fields.Nested(auth_relationships)
})

login_data = api.model('login_data', {
    "type": fields.String(),
    "data": fields.Nested(login_data_content)
})

logout_user = api.model('logout_user', {'success': fields.String()})


@api.errorhandler(EmailConflictError)
@api.marshal_with(register_error, code=409, description="Email already used")
def handle_email_conflict_exception(error):
    """This is an email conflict error"""
    return {'message': error.message}, 409


@api.errorhandler(WrongPasswordValidationError)
@api.marshal_with(register_error, code=401, description="Email already used")
def handle_email_conflict_exception(error):
    """This is a wrong password error"""
    return {'message': error.message}, 401


@api.errorhandler(UserTokenFailedError)
@api.marshal_with(register_error, code=401, description="Unauthorized")
def handle_email_conflict_exception(error):
    """This is a login error"""
    return {'message': error.message}, 401


@api.errorhandler(UserNotFoundError)
@api.marshal_with(register_error, code=404, description="User not found")
def handle_email_conflict_exception(error):
    """This is a user existence error"""
    return {'message': error.message}, 404


@api.errorhandler(CreateFailedError)
@api.marshal_with(register_error, code=500, description="User couldn't be created")
def handle_entity_processing_exception(error):
    """This is an unknown error"""
    return {'message': error.message}, 500


@api.errorhandler(UnknownAuthError)
@api.marshal_with(register_error, code=500, description="Internal server error")
def handle_internal_server_exception(error):
    """This is an internal server error"""
    return {'message': error}, 500


@api.route('/register')
class RegisterRestApi(Resource):
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
    def post(self):
        if not request.is_json:
            return make_bad_request_response(APIError.WRONG_API)
        new_user, new_token = RegisterUserCommand(request.json).run()
        response_obj = {
            "id": new_user.id,
            "attributes": {
                "email": new_user.email,
                "is_admin": new_user.is_admin
            },
            "relationships": {
                "token": {
                    "token": new_token.token,
                }
            },
        }
        return self.response_creator.response_201(response_obj)


@api.route('/login')
class LoginRestApi(Resource):
    """Login existing user"""

    response_creator = UltimateServerResponseCreator('auth')

    @api.doc('login_user', responses={
        201: 'Success',
        400: 'Wrong API',
        401: 'Login failed',
        409: 'User already logged in',
        500: 'Internal server'
    })
    @api.expect(login_request, validate=True)
    @api.marshal_with(login_data, code=201, description="User logged in")
    def post(self):
        if not request.is_json:
            return make_bad_request_response(APIError.WRONG_API)
        user, token = LoginUserCommand(request.json).run()
        response_obj = {
            "id": user.id,
            "attributes": {
                "email": user.email,
                "is_admin": user.is_admin
            },
            "relationships": {
                "token": {
                    "token": token.token,
                }
            },
        }
        return self.response_creator.response_201(response_obj)


@api.route('/logout')
class LogoutRestApi(Resource):
    """Logout user"""

    response_creator = UltimateServerResponseCreator('auth')

    @token_required
    @api.doc('logout_user', responses={
        200: 'Success',
        400: 'Wrong API',
        401: 'Logout failed',
        500: 'Internal server'
    })
    @api.doc(security='apikey')
    def delete(self, current_user, users_token):
        logout_response = LogoutUserCommand(users_token).run()
        return self.response_creator.response_200(logout_response)
