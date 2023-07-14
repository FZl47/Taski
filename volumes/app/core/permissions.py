

def permission_method(classes):
    def inner(func):
        def wrapper(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return wrapper
    return inner