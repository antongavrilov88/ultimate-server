from flask import request
from flask_restx import Resource, Namespace, fields, reqparse

api = Namespace('auth', description='Authorization related operations')

register_request = api.model('register_request', {
    'email': fields.String(description='The task...'),
    'password': fields.String(description='The task...'),
})

register_data = api.model('register_data', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(readonly=True, description='The task...'),
    'password': fields.String(readonly=True, description='The task...'),
})


@api.route('/register')
class AuthRestApi(Resource):
    """Register new user"""

    @api.doc('register_user')
    @api.expect(register_request)
    @api.marshal_with(register_data, code=201)
    def post(self):
        if not request.is_json:
            return self.response_400(message='Request is not JSON')
        return {'register': '123'}
