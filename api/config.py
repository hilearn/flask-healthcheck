class Config:
    subclasses = []

    def __init_subclass__(cls):
        Config.subclasses.append(cls)

    @classmethod
    def check_env(cls, env):
        return cls.env == env

    env = 'development'

    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = 'spec'
    OPENAPI_REDOC_PATH = 'redoc'
    OPENAPI_REDOC_VERSION = 'next'
    OPENAPI_SWAGGER_UI_PATH = 'swagger'
    OPENAPI_SWAGGER_UI_VERSION = '3.19.5'


class StagingConfig(Config):
    env = 'staging'


def get_config(env):
    for subclass in Config.subclasses:
        if subclass.check_env(env):
            return subclass
    return Config
