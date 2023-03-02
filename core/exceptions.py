from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        detail = exc.get_full_details()
        status_code = detail.get('status',{}).get('message') or response.status_code
        messages = [m['message'] for m in detail.get('messages',{})]
        if not messages:
            messages = [detail.get('message')]
        if not any(messages):
            messages = []
        response.data = {
            'result':{},
            'messages':messages,
            'status':status_code
        }
    return response


def _execption_detail(status_code,messages=[]):
    return {
        'result':{},
        'status':status_code,
        'messages':messages
    }


def get_messages_serializer(errors):
    return [str(err[0]) for err in errors.values()]


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
    default_detail = _execption_detail(status_code,['Bad request'])


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


class InvalidFormatFile(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "format_file_not_valid"
    default_detail = _execption_detail(status_code,['Format file is invalid'])


class InvalidEmail(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "email_not_valid"
    default_detail = _execption_detail(status_code,['Email is invalid'])


class InvalidField(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "field_not_valid"
    default_detail = _execption_detail(status_code,['Field is invalid'])


class FieldRequired(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "field_required"
    default_detail = _execption_detail(status_code,['Field is required'])

