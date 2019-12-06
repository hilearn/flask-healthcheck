import os
from flask import Flask
from api.config import get_config
from .v1 import blp, auth_scheme
from flask_smorest import Api


app = Flask(__name__)


# Ignore 'ENV' == 'production' if it is not set by the user.
if os.environ.get('FLASK_ENV') is None:
    os.environ['FLASK_ENV'] = app.config['ENV'] = 'sandbox'


config_cls = get_config(app.config['ENV'])

app.config.from_object('.'.join([config_cls.__module__, config_cls.__name__]))


api = Api(app)

api.spec.components.security_scheme(*auth_scheme)

api.register_blueprint(blp, url_prefix='/')
