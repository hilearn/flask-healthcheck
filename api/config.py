class DevelopmentConfig:
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = 'spec'
    OPENAPI_SWAGGER_UI_PATH = 'swagger'
    OPENAPI_SWAGGER_UI_VERSION = '3.19.5'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'


class StagingConfig(DevelopmentConfig):
    pass
