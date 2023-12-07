from os import environ, path


basedir = path.abspath(path.dirname(__file__))

class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or b'secret'
    FLASK_SECRET = SECRET_KEY

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'instance/db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'instance/db.sqlite')

class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'instance/db_test.sqlite')
    WTF_CSRF_ENABLED = False

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test' : TestConfig
}