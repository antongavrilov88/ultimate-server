import os
from enum import IntEnum
from dotenv import load_dotenv
#
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

server_postgres_base = os.getenv('SERVER_DATABASE_URL', None)
server_database_name = 'antondb'

api_prefix = 'api'

api_version_major = 1
api_version_minor = 0
api_version_str = "%d.%d" % (api_version_major, api_version_minor)
api_version_prefix = api_prefix + '/v' + api_version_str


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_awesome_server')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = server_postgres_base + server_database_name
    SQLALCHEMY_BINDS = {
        'my_awesome_server': server_postgres_base + server_database_name
    }


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = server_postgres_base + server_database_name + '_test'
    SQLALCHEMY_BINDS = {
        'my_awesome_server': server_postgres_base + server_database_name + '_test'
    }
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = 'my_awesome_server'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = server_postgres_base + server_database_name
    SQLALCHEMY_BINDS = {
        'my_awesome_server': server_postgres_base + server_database_name
    }