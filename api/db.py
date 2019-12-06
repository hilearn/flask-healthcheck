TOKEN_DB = {
    'hiSecret': {'email': 'user@example.com'},
    'hiVerySecret': {'email': 'admin@example.com'},
}


def auth_token(token):
    return TOKEN_DB.get(token)
