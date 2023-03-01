from rest_framework.exceptions import APIException
from rest_framework import status

def _execption_detail(status_code,messages=[]):
    return {
        'result':{},
        'status':status_code,
        'messages':messages
    }

class DetailDictMixin:
    def __init__(self,messages=[],status_code=None,default_code=None):

        if status_code != None:
            setattr(self,'status_code',status_code)
        else:
            status_code = self.status_code

        messages = messages or self.default_detail.get('messages')
        default_code = default_code or self.default_code
        detail_dict = _execption_detail(status_code,messages)
        super().__init__(detail_dict)


class Exception(DetailDictMixin,APIException):
    pass


class BadRequest(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "bad_request"
    default_detail = _execption_detail(status_code,['Bad request check fields'])


class AuthenticationNotProvided(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "authentication_not_provided"
    default_detail = _execption_detail(status_code,['Authentication credentials were not provided'])


class AuthenticationFailed(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "authentication_failed"
    default_detail = _execption_detail(status_code,['Authorization failed'])


class InvalidToken(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = "token_is_not_valid"
    default_detail = _execption_detail(status_code,['Token is invalid'])