from flask_smorest import Blueprint
from flask.views import MethodView

from .db import auth_token
from .auth import create_basic_header_auth


blp = Blueprint('Health check API', __name__,
                description='API Endpoints for demonstration and health '
                            'checking of services.')


auth_schema, auth_required = create_basic_header_auth(blp, 'AuthToken', auth_token)


@blp.route('/')
class HealthCheck(MethodView):
    @blp.response()
    def get(self):
        return {
            "status": "healthy"
        }

    @auth_required(propagate_account=True)
    @blp.response()
    def post(self, account):
        return {
            "status": "healthy",
            "hello": account,
        }
