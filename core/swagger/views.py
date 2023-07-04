from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action

_VIEWS = []
_ALLOW_METHODS = ['post','get','put','delete']
_SWAGGER_INITIALIZED = False


class SwaggerMixin:
    pass


def init():
    global _SWAGGER_INITIALIZED
    if _SWAGGER_INITIALIZED is False:
        _SWAGGER_INITIALIZED = True
        _VIEWS = SwaggerMixin.__subclasses__()
        for view in _VIEWS:
            SWAGGER = view.SWAGGER
            methods = SWAGGER['methods'].keys()
            tags = SWAGGER['tags']
            for method in methods:
                if hasattr(view,method):
                    SWAGGER_CONF = SWAGGER['methods'][method].copy()
                    method = method.lower()
                    method_func = getattr(view, method)
                    # Chane name arguments data to original name
                    SWAGGER_CONF['operation_id'] = SWAGGER_CONF['title']
                    SWAGGER_CONF['operation_description'] = SWAGGER_CONF.get('description',view.__doc__)
                    # Remove unless arguments
                    del SWAGGER_CONF['title']
                    del SWAGGER_CONF['description']
                    SWAGGER_CONF['tags'] = tags
                    SWAGGER_CONF['security'] = SWAGGER.get('security',None)
                    method_func = swagger_auto_schema(**SWAGGER_CONF)(method_func)
                    setattr(view, method, method_func)

