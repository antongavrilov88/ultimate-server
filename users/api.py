from flask_restx import Resource, Namespace, fields


api = Namespace('users', description='Users related operations')


@api.route('/hello_get')
class HelloWorld(Resource):
    get_users_schema = api.model('UserGetResponseSchema', {
        'id': fields.Integer,
        'email': fields.String
    })

    @api.marshal_with(get_users_schema)
    def get(self):
        try:
            return {'hello': 'get'}
        except Exception as er:
            pass


@api.route('/hello_post')
class HelloWorld(Resource):

    def post(self):
        return {'hello': 'post'}
