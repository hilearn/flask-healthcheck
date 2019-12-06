from functools import wraps
from flask_smorest import abort
from flask import request
from copy import deepcopy


def token_header_auth(blp, token_key, authenticate_func,
                      auth_schema_name='TokenAuth'):

    def decorator_constructor(propagate_account=False):
        def decorator(method):
            @wraps(method)
            def replacement(self):
                token = request.headers.get(token_key)

                if token is None:
                    abort(401)

                account = authenticate_func(token)

                if propagate_account:
                    return method(self, account)
                else:
                    return method(self)

            replacement._apidoc = deepcopy(getattr(replacement, '_apidoc', {}))
            replacement._apidoc.setdefault('security', []).append(
                {auth_schema_name: []})

            return replacement
        return decorator

    security_scheme = (auth_schema_name, {"in": "header",
                                          "name": token_key,
                                          "type": 'apiKey'})
    return security_scheme, decorator_constructor
