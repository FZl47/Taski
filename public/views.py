from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.response import Response
from core.mixins.view.swagger import  SwaggerMixin



class Index(SwaggerMixin, APIView):

    SWAGGER = {
        'tags': ['Test Health'],
        'methods': {
            'post': {
                'title': 'Test health project POST',
                'description':'',
                # 'request_body': X,  # serizlier or instance
                'responses': {
                    200:"",
                },
            },
            'get': {
                'title': 'Test health project GET',
                'description':'',
                #'query_serializer': X,  # serizlier or instance
                'responses': {
                    200: "",
                },
            },

        }
    }

    permission_classes = (IsAuthenticated,)


    def post(self, request):
        """
            Test view
        """
        return Response('Hi')

    def get(self, request):
        """
            Test view
        """
        return Response('Hi')
