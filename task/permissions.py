from rest_framework.permissions import BasePermission
from core import exceptions
from . import models


class IsOwnerGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id')
        try:
            group = models.Group.objects.get(id=group_id,owner=request.user)
            # set group attr for use later in view
            setattr(request,'group',group)
        except:
            raise exceptions.PermissionDenied(['Only group owner can access or Group Not found with this ID'])
        return True

class IsOwnerOrAdminGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id')
        try:
            group = models.Group.objects.get(id=group_id,owner=request.user)
            # set group attr for use later in view
            setattr(request,'group',group)
        except:
            raise exceptions.PermissionDenied(['Only group owner or admins can access or Group Not found with this ID'])
        return True