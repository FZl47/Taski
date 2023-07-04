from rest_framework.views import APIView
from rest_framework import permissions
from core.response import Response
from core.swagger.views import SwaggerMixin
from core.views import BaseView
from . import swagger


class Index(BaseView,APIView):
    METHOD_NAMES = ('post','get')
    SWAGGER = swagger.INDEX

    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        """
            Test view
        """
        return Response('is working ...')

    def get(self, request):
        """
            Test view
        """
        return Response('is working ...')


