from flask_restx import Api
from users.api import api as users_api
from auth.api import api as auth_api

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(sequrity='Bearer Auth', authorizations=authorizations, title="AGwallet API", version="1.0",
          description="Project API")

api.add_namespace(auth_api)
api.add_namespace(users_api)
