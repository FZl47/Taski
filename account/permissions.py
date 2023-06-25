from rest_framework.permissions import BasePermission
from core.models import get_object_or_none
from core import exceptions
from . import models


class IsOwnerGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id') or request.data.get('group_id')
        group = get_object_or_none(models.Group,id=group_id)
        owner = get_object_or_none(models.GroupAdmin,is_owner=True,user=request.user,group=group)
        if group is None:
            raise exceptions.NotFound(['Group Not found with this ID'])
        if owner is None:
            raise exceptions.PermissionDenied(['Only group owner can access.'])
        # set group attr for use in view
        setattr(request, 'group', group)
        setattr(request, 'admin', owner)  # group admin object
        setattr(request, 'is_owner_group', True)  # is Owner
        return True


class IsOwnerOrAdminGroup(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id') or request.data.get('group_id')
        group = get_object_or_none(models.Group, id=group_id)
        if group is None:
            raise exceptions.NotFound(['Group Not found with this ID'])
        admin = get_object_or_none(models.GroupAdmin, user=request.user, group=group)
        if admin is None:
            raise exceptions.PermissionDenied(['Only group owner or admins can access.'])
        # set group attr for use in view
        setattr(request, 'group', group)
        setattr(request, 'admin', admin)
        setattr(request, 'is_owner_group', admin.is_owner)  # Admin or Owner
        return True


class IsMemberShip(BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get('group_id') or request.data.get('group_id')
        group = get_object_or_none(models.Group, id=group_id)
        if group is None:
            raise exceptions.NotFound(['Group Not found with this ID'])
        membership = get_object_or_none(models.User, id=request.user.id,groups_task__id__in=[group.id])
        if membership is None:
            raise exceptions.PermissionDenied(['Only membership of the group can access.'])
        # set group attr for use in view
        setattr(request, 'group', group)
        return True
