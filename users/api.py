from flask_restx import Resource

from api.UltimateServerResponseCreator import UltimateServerResponseCreator
from commands.exceptions import ObjectNotFoundError
from models.user import User
from users.commands.get_list import GetUsersListCommand
from users.commands.get_user import GetUserCommand
from utils.admin_access_required import admin_access_required
from utils.token_required import token_required
from .commands.exceptions import AccessDeniedError, UserAuthorizationError, GetUsersListError, UserNotFound
from flask_restx import Namespace
from flask_restx import fields

api = Namespace('users', description='Users related operations')


user_attributes = api.model('user_attributes', {
    'email': fields.String(),
    'is_admin': fields.Boolean()
})

get_user_schema = api.model('get_user_schema', {
    'type': fields.String(),
    'id': fields.Integer,
    'attributes': fields.Nested(user_attributes)
})

user_data_details = api.model('user_data_details', {
    'id': fields.Integer(),
    'attributes': fields.Nested(user_attributes)
})

get_users_schema = api.model('get_users_schema', {
    'type': fields.String(),
    'data': fields.Raw({
        'id': 1,
        'attributes': {
            'email': 'string',
            'is_admin': False
        }
    })
})

get_user_by_id_schema = api.model('get_user_by_id_schema', {
    'type': fields.String(),
    'data': fields.Nested(user_data_details)
})

register_error: object = api.model('register_error', {
    'message': fields.String(readonly=True)
})


@api.errorhandler(AccessDeniedError)
@api.marshal_with(register_error, code=403, description="Forbidden.")
def handle_email_conflict_exception(error):
    print(1, error)
    """This is an email conflict error"""
    return {'message': error.message}, 403


@api.errorhandler(UserNotFound)
@api.marshal_with(register_error, code=404, description="Forbidden.")
def handle_email_conflict_exception(error):
    print(1, error)
    """This is an email conflict error"""
    return {'message': error.message}, 404


@api.errorhandler(UserAuthorizationError)
@api.marshal_with(register_error, code=401, description="Unauthorized")
def handle_email_conflict_exception(error):
    print(2, error)
    """This is a login error"""
    return {'message': error.message}, 401


@api.errorhandler(GetUsersListError)
@api.marshal_with(register_error, code=500, description="Request failed")
def handle_entity_processing_exception(error):
    print(3, error)
    """This is an unknown error"""
    return {'message': error.message}, 500


@api.errorhandler(Exception)
@api.marshal_with(register_error, code=500, description="Internal server error")
def handle_internal_server_exception(error):
    print(4, error)
    """This is an internal server error"""
    return {'message': error}, 500


@api.route('/')
class UsersRestApi(Resource):
    """Get list of users and create user"""

    response_creator = UltimateServerResponseCreator('users')

    @token_required
    @admin_access_required
    @api.doc('get_users', responses={
        200: 'Success',
        400: 'Wrong API',
        401: 'Unauthorized',
        403: 'Access denied',
        500: 'Internal server'
    })
    @api.doc(security='apikey')
    @api.marshal_with(get_users_schema, code=200, description="Users list")
    def get(self, current_user, users_token):
        users_list = GetUsersListCommand(user=current_user, token=users_token).run()
        return self.response_creator.response_200(
            list(map(lambda user: User.get_data(user, minimal=False), users_list)))


@api.route('/<int:user_id>')
class UserRestApi(Resource):
    """Get and update user data and delete user"""

    response_creator = UltimateServerResponseCreator('users')

    @token_required
    @admin_access_required
    @api.doc('get_user', responses={
        200: 'Success',
        400: 'Wrong API',
        401: 'Unauthorized',
        403: 'Access denied',
        500: 'Internal server'
    })
    @api.doc(security='apikey')
    @api.marshal_with(get_user_by_id_schema, code=200, description="User")
    def get(self, current_user, users_token, user_id):
        user = GetUserCommand(user_id).run()
        return self.response_creator.response_200(User.get_data(user, minimal=False))
