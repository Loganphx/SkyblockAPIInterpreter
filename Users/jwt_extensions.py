import jwt
import uuid
import warnings

from _cffi_backend import callback
from django.contrib.auth import get_user_model

from calendar import timegm
from datetime import datetime

from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse, HttpRequest
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    username_field = get_username_field()
    username = get_username(user)
    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )

    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if hasattr(user, 'last_name'):
        payload['last_name'] = user.last_name
    if hasattr(user, 'first_name'):
        payload['first_name'] = user.first_name
    if hasattr(user, 'userRole'):
        payload['userRole'] = user.userRole
    if hasattr(user, 'discordID'):
        payload['discordID'] = user.userRole
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)
    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    """
    django_response = HttpRequest()
    django_response.token = token
    print(django_response.token)
    request.session.create()
    print(request.user)
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {
        'token': token
    }
