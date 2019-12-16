import os
from flask import Flask
from flask import g, make_response, request
from api.config import get_config
from werkzeug import ImmutableMultiDict
from pyinstrument import Profiler
from .v1 import blp, auth_scheme
from flask_smorest import Api


app = Flask(__name__)


# Ignore 'ENV' == 'production' if it is not set by the user.
if os.environ.get('FLASK_ENV') is None:
    os.environ['FLASK_ENV'] = app.config['ENV'] = 'sandbox'


config_cls = get_config(app.config['ENV'])

app.config.from_object('.'.join([config_cls.__module__, config_cls.__name__]))


# add ?profile to the end of a request URL to activate the profiler
@app.before_request
def before_request():
    if "profile" in request.args:
        request.args = ImmutableMultiDict([
            (k, v) for k, v in request.args.items() if k != 'profile'])
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if not hasattr(g, "profiler"):
        return response
    g.profiler.stop()
    output_html = g.profiler.output_html()
    return make_response(output_html)


api = Api(app)

api.spec.components.security_scheme(*auth_scheme)

api.register_blueprint(blp, url_prefix='/')
