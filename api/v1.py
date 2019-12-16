from flask_smorest import Blueprint
from flask.views import MethodView

from .db import auth_token
from .auth import token_header_auth

from .schema import GreetingArgs, Reply, ReplySchema, GreetingType


blp = Blueprint('Health check API', __name__,
                description='API Endpoints for demonstration and health '
                            'checking of services.')

auth_scheme, auth_required = token_header_auth(blp, 'AuthToken', auth_token)


@blp.route('/')
class HealthCheck(MethodView):
    @blp.response()
    def get(self):
        """
        get request to check that the server is running.
        """
        return {
            "status": "healthy"
        }


@blp.route('/greet')
class Greeting(MethodView):
    replies = {
        GreetingType.FORMAL: 'Hello',
        GreetingType.CAUSAL: 'Hey',
    }

    @blp.arguments(GreetingArgs, location='query', required=True,
                   as_kwargs=True)
    @blp.response(ReplySchema)
    def get(self, greeting_type=GreetingType.FORMAL):
        """
        customized greeting message
        """
        return Reply(greeting_type=greeting_type,
                     message=self.replies[greeting_type])

    @auth_required(propagate_account=True)  # Order matters
    @blp.arguments(GreetingArgs, location='json', required=True,
                   as_kwargs=True, example={'greeting_type': 'formal'})
    @blp.response(ReplySchema)
    def post(self, account, greeting_type):
        """
        user customized greeting
        """
        return Reply(greeting_type=greeting_type,
                     user=account,
                     message=self.replies[greeting_type])
