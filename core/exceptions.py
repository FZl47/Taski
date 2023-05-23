from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        try:
            detail = exc.get_full_details()
            status_code = detail.get('status', {}).get('message') or response.status_code
            messages = [m['message'] for m in detail.get('messages', {})]
            if not messages:
                messages = [detail.get('message')]
            if not any(messages):
                messages = []
            response.data = {
                'result': {},
                'messages': messages,
                'status': status_code
            }
        except:
            return response
    return response


def _execption_detail(status_code,messages=[]):
    return {
        'result':{},
        'status':status_code,
        'messages':messages
    }


def get_messages_serializer(errors):
    result = []
    for field_name,err_mess in errors.items():
        field_name = str(field_name)
        err_mess = str(err_mess[0])
        err_mess = f"{field_name} => {err_mess}"
        result.append(err_mess)
    return result


def serializer_err(serializer):
    messages = []
    for err in serializer.errors.items():
        messages.append(
            "{} : {}".format(err[0],err[1][0])
        )
    return messages

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


class InvalidFormatImage(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "format_image_not_valid"
    default_detail = _execption_detail(status_code,['Format image is invalid'])


class InvalidEmail(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "email_not_valid"
    default_detail = _execption_detail(status_code,['Email is invalid'])


class InvalidField(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "field_not_valid"
    default_detail = _execption_detail(status_code,['Field is invalid'])


class InvalidCode(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "code_reset_password_not_valid"
    default_detail = _execption_detail(status_code,['Code reset password is invalid'])


class FieldRequired(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "field_required"
    default_detail = _execption_detail(status_code,['Field is required'])


class NotFound(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "not_found"
    default_detail = _execption_detail(status_code,['Not found'])


class UserNotFound(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "user_not_found"
    default_detail = _execption_detail(status_code,['User not found'])


class AdminGroupNotFound(Exception):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "admin_group_not_found"
    default_detail = _execption_detail(status_code,['Admin Group not found'])


class PermissionDenied(Exception):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "permission_denied"
    default_detail = _execption_detail(status_code, ['Permission Denied'])


class Conflict(Exception):
    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"
    default_detail = _execption_detail(status_code,['Conflict'])

