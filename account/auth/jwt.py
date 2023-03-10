from rest_framework_simplejwt.authentication import (
    JWTAuthentication as _JWTAuthentication,
    AUTH_HEADER_TYPE_BYTES,
    HTTP_HEADER_ENCODING,
    AUTH_HEADER_TYPES,
    api_settings,
    get_user_model
)
from core import exceptions


class JWTAuthentication(_JWTAuthentication):
    """
        Custom JWT autnetication
    """

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            return None
            # raise exceptions.AuthenticationNotProvided

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
            # raise exceptions.AuthenticationNotProvided

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token



    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(['Authorization header must contain two space-delimited values'])

        return parts[1]

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except:
                raise exceptions.InvalidToken

        raise exceptions.InvalidToken

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise exceptions.InvalidToken(["Token contained no recognizable user identification"])
        try:

            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise exceptions.AuthenticationFailed(["User not found"])

        if not user.is_active:
            raise exceptions.AuthenticationFailed(["User is inactive"])

        return user



