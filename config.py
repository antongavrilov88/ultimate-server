import os
from enum import IntEnum
from dotenv import load_dotenv
#
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

agwallet_postgres_base = os.getenv('AGWALLET_DATABASE_URL', None)
agwallet_database_name = 'antondb'

api_prefix = 'api'

api_version_major = 1
api_version_minor = 0
api_version_str = "%d.%d" % (api_version_major, api_version_minor)
api_version_prefix = api_prefix + '/v' + api_version_str


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = agwallet_postgres_base + agwallet_database_name
    SQLALCHEMY_BINDS = {
        'agwallet': agwallet_postgres_base + agwallet_database_name
    }


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = agwallet_postgres_base + agwallet_database_name + '_test'
    SQLALCHEMY_BINDS = {
        'agwallet': agwallet_postgres_base + agwallet_database_name + '_test'
    }
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = agwallet_postgres_base + agwallet_database_name
    SQLALCHEMY_BINDS = {
        'agwallet': agwallet_postgres_base + agwallet_database_name
    }