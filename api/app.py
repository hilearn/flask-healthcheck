import os
from flask import Flask
from api.config import get_config
from .v1 import blp
from flask_smorest import Api


app = Flask(__name__)


# Ignore 'ENV' == 'production' if it is not set by the user.
if os.environ.get('FLASK_ENV') is None:
    os.environ['FLASK_ENV'] = app.config['ENV'] = 'sandbox'


config_cls = get_config(app.config['ENV'])

app.config.from_object('.'.join([config_cls.__module__, config_cls.__name__]))


api = Api(app)
api.register_blueprint(blp, url_prefix='/')
