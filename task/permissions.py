from rest_framework.permissions import BasePermission
from core.models import get_object_or_none
from core import exceptions
from . import models


class IsOwnerGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id')
        group = get_object_or_none(models.Group,id=group_id, owner=request.user)
        if group:
            # set group attr for use in view
            setattr(request,'group',group)
            setattr(request,'is_owner_group',True) # is Owner
        else:
            raise exceptions.PermissionDenied(['Only group owner can access or Group Not found with this ID'])
        return True


class IsOwnerOrAdminGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id')
        group = get_object_or_none(models.Group, id=group_id, owner=request.user)
        if group:
            setattr(request, 'is_owner_group', True)  # is Owner
        else:
            group = get_object_or_none(models.Group, id=group_id, admins__group=request.user)
            setattr(request, 'is_owner_group', False)  # is Admin
        # set group attr for use in view
        if group is None:
            raise exceptions.PermissionDenied(['Only group owner or admins can access or Group Not found with this ID'])
        setattr(request, 'group', group)
        return True