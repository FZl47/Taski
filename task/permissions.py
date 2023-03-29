from rest_framework.permissions import BasePermission
from core import exceptions
from . import models


class IsOwnerGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id')
        try:
            group = models.Group.objects.get(id=group_id,owner=request.user)
            setattr(request,'group',group)
        except:
            raise exceptions.PermissionDenied(['Only owner group can access'])
        return True