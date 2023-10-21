from flask import request, abort, json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
from dotenv import find_dotenv, load_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev-6gmv1a0co3vnyslf.us.auth0.com')
ALGORITHMS = os.getenv('ALGORITHMS', ['RS256'])
API_AUDIENCE = os.getenv('API_AUDIENCE', 'coffee_shop_api')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    # ref: Full Stack Web Developer/
    #   Identity Access Management/
    #       Identity and Authentication
    #           13. Sending token
    # check if authorization is not in request

    if 'Authorization' not in request.headers:
        abort(401)
    # get the token
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    # check if token is valid
    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)
    return header_parts[1]


def check_permissions(permission, payload):
    # Check if the payload contains the permissions key
    if 'permissions' not in payload:
        abort(401)

    # Check if the required permission is in the user's permissions
    if permission not in payload['permissions']:
        abort(401)

    # If the user has the required permission, return True
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/',
                # options={'verify_signature': False},
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'The token is expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'The claims are invalid.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'The token is invalid.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'The JWT does not contain the proper action'
            }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
