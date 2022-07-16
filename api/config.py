import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class BaseConfig():

    SQLALCHEMY_DATABASE_URI = 'postgresql://anton:anton1234@localhost:5432/antondb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "flask-app-secret-key-change-it"
    JWT_SECRET_KEY = "jwt-app-secret-key-change-it"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
