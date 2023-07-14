from functools import wraps
from drf_yasg.utils import swagger_auto_schema


class SwaggerView:
    """
        SWAGGER: example config => {
                'tags': ['...'],
                'methods':{
                    'post': {
                        'title': '...',
                        'description': '...',
                        'request_body': ...,
                        'responses': {
                            200: ...
                        },
                    }
                }
            }
    """

    @classmethod
    def set_config(cls, view, config, tags=None):
        methods = config['methods'].keys()
        tags = config.get('tags', tags)
        for method in methods:
            if hasattr(view, method):
                method_conf = config['methods'][method].copy()
                # method = method.lower()
                method_func = getattr(view, method)
                # Chane name arguments data to original name
                method_conf['operation_id'] = method_conf['title']
                method_conf['operation_description'] = method_conf.get('description', view.__doc__)
                # Remove unless arguments
                del method_conf['title']
                del method_conf['description']
                method_conf['tags'] = tags
                method_conf['security'] = config.get('security', None)
                method_func = swagger_auto_schema(**method_conf)(method_func)
                setattr(view, method, method_func)


class SwaggerBaseView:
    """
    SWAGGER: example config => {
            'tags': ['...'],
            'views': {
                'Create':{
                    'methods':{
                        'post': {
                        'title': '...',
                        'description': '...',
                        'request_body': ...,
                        'responses': {
                            200: ...
                        },
                    }
                }
            }
        }
    """

    @classmethod
    def set_config(cls, base_view, config):
        tags = config['tags']
        view_names = config['views'].keys()
        views = []
        for view_name in view_names:
            view = getattr(base_view, view_name, None)
            if view is None:
                raise Exception('View not found with this name %s in BaseView %s' % (view_name, base_view.__name__))
            views.append(view)
        for view in views:
            view_config = config['views'][view.__name__]
            SwaggerView.set_config(view, view_config, tags=tags)
