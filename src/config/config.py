import os
from datetime import timedelta
# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname('src'))

class Config:
    SECRET_KEY= os.environ.get("SECRET_KEY")
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    Swagger = { 
                "title":"Flask REST API template",
                "uiversion" : 3
              }


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ.get("SQLAlchemy_Dev_DB"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/bookmarks'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456@localhost/bookmarks'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY