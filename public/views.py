from rest_framework.views import APIView
from rest_framework import permissions
from core.response import Response
from core.mixins.view.swagger import  SwaggerMixin



class Index(SwaggerMixin, APIView):

    SWAGGER = {
        'tags': ['Test Health'],
        'methods': {
            'post': {
                'title': 'Test health project POST',
                'description':'',
                'responses': {
                    200:"",
                },
            },
            'get': {
                'title': 'Test health project GET',
                'description':'',
                'responses': {
                    200: "",
                },
            },

        }
    }

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
