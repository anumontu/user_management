from rest_framework.exceptions import APIException


class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'Authentication Failed'
    default_code = 'authentication_failed'


class AuthorizationFailed(APIException):
    status_code = 403
    default_detail = 'authorization_failed'
    default_code = 'Authorization Failed'
