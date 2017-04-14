import os

PROJECT_NAME = "ensemblefeedback"
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ensemblefeedback"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://localhost/ensemblefeedback"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/ensemblefeedback"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://localhost/ensemblefeedback"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DebugConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://localhost/ensemblefeedback"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
