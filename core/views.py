from .swagger.utils import SwaggerView


class BaseView:
    """
        Just For (DRY)
        :attribute: VIEW_NAMES
        :attribute: SWAGGER
        :attribute: use_child_permission
        :attribute: use_child_parser
        :attribute: permission_classes
        :attribute: permission_classes_additional
        :attribute: parser_classes

        VIEW_NAMES: ('Create','Update',...)

        SWAGGER: Swagger Config => {
            'tags': ['...'],
            'methods': {
                'post': {
                    'title': '...',
                    'description': '...',
                    'request_body': ...,
                    'responses': {
                        200: ...
                    },
                },
            }
        }

        use_child_permission: if you want to use 'permission' or 'permission_classes_additional' in subclass(Create,Update,...)
        set it True

        permission_classes: you can set 'permission_classes' in BaseView or set in subclass(Create,Update,...)
        if you set this in BaseView other subclasses follow that

        permission_classes_additional: you can set 'permission_classes_additional' in BaseView or set in subclass(Create,Update,...)
        if you set this in BaseView other subclasses follow that
        this means that you can add new permissions in addition to the default permissions

        parser_classes: you can set 'parser_classes' in BaseView or set in subclass(Create,Update,...)
        if you set this in BaseView other subclasses follow that
    """
    pass


def init_config_base_view():
    base_views = BaseView.__subclasses__()
    for base_view in base_views:
        view_names = getattr(base_view, 'VIEW_NAMES', None)
        if view_names is None:
            raise ValueError('attribute VIEW_NAMES must be set')
        swagger = getattr(base_view, 'SWAGGER', None)
        permission_classes_base = getattr(base_view, 'permission_classes', None)
        permission_classes_additional_base = getattr(base_view, 'permission_classes_additional', None)
        assert permission_classes_base is None or permission_classes_additional_base is None, 'You can just use one of them(permission_classes or permission_classes_additional)'
        parser_classes = getattr(base_view, 'parser_classes', None)
        for view_name in view_names:

            view = getattr(base_view, view_name, None)

            if view is None:
                raise ValueError('view not found with this name %s' % view_name)

            use_child_permission = getattr(view, 'use_child_permission', False)
            if use_child_permission:
                permission_classes_additional = getattr(view, 'permission_classes_additional', None)
                if permission_classes_additional:
                    permission_classes = getattr(view, 'permission_classes', [])
                    permission_classes = list(permission_classes) + list(permission_classes_additional)
                    setattr(view, 'permission_classes', permission_classes)
            else:
                if permission_classes_base:
                    setattr(view, 'permission_classes', permission_classes_base)
                else:
                    if permission_classes_additional_base:
                        permission_classes = getattr(view, 'permission_classes', [])
                        permission_classes = list(permission_classes) + list(permission_classes_additional_base)
                        setattr(view, 'permission_classes', permission_classes)

            if parser_classes:
                use_child_parser = getattr(view, 'use_child_parser', False)
                if use_child_parser is False:
                    setattr(view, 'parser_classes', parser_classes)

            if swagger:
                SwaggerView.set_config(view, swagger)