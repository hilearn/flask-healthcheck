from flask_smorest import Blueprint
from flask.views import MethodView

from .db import auth_token
from .auth import token_header_auth

from .schema import GreetingArgs, Reply, GreetingType


blp = Blueprint('Health check API', __name__,
                description='API Endpoints for demonstration and health '
                            'checking of services.')

auth_scheme, auth_required = token_header_auth(blp, 'AuthToken', auth_token)


@blp.route('/')
class HealthCheck(MethodView):
    @blp.response(description='return status')
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

    @blp.arguments(GreetingArgs.schema, location='query', required=True,
                   as_kwargs=True)
    @blp.response(Reply.schema,
                  description='Return greeting message.')
    def get(self, greeting_type):
        return Reply(greeting_type=greeting_type,
                     message=self.replies[greeting_type])

    @auth_required(propagate_account=True)  # Order matters
    @blp.arguments(GreetingArgs.schema, location='json', required=True,
                   as_kwargs=True, example={'greeting_type': 'formal'})
    @blp.response(Reply.schema,
                  description='Return user customized greeting message.')
    def post(self, account, greeting_type):
        return Reply(greeting_type=greeting_type,
                     user=account,
                     message=self.replies[greeting_type])
