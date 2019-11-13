from flask_smorest import Blueprint
from flask.views import MethodView


blp = Blueprint('Health check API', __name__,
                description='API Endpoints for demonstration and health '
                            'checking of services.')


@blp.route('/')
class HealthCheck(MethodView):
    def get(self):
        return {
            "status": "healthy"
        }
