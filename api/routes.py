from flask_restx import Api

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

rest_api = Api(sequrity='Bearer Auth', authorizations=authorizations, version='1.0', title='AGwallet API')