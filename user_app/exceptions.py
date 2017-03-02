from rest_framework.exceptions import APIException


class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'Authentication Failed'
    default_code = 'authentication_failed'
