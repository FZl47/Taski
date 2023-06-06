from django.urls import path
from . import views


app_name = 'task'
urlpatterns = [
    # Group
    path('group/create',views.CreateGroup.as_view(),name='create_group'),
    path('group/<uuid:group_id>/delete',views.DeleteGroup.as_view(),name='delete_group'),
    # Group User
    path('group/<uuid:group_id>/users',views.GroupUsers.as_view(),name='group_users'),
    path('group/<uuid:group_id>/users/add/request',views.RequestAddUserToGroup.as_view(),name='request_add_user_group'),
    path('group/<uuid:group_id>/users/<uuid:user_id>/delete',views.DeleteGroupUser.as_view(),name='group_user_delete'),
    # Admin
    path('group/admin/create',views.CreateAdminGroup.as_view(),name='create_admin_group'),
    path('group/<uuid:group_id>/admins/add',views.AddAdminToGroup.as_view(),name='add_admin_to_group'),
    path('group/<uuid:group_id>/admins/<uuid:admin_id>/delete',views.DeleteGroupAdmin.as_view(),name='group_admin_delete'),
    path('group/<uuid:group_id>/admins',views.GroupAdmins.as_view(),name='group_admins'),
    # path('group/<str:group_id>/admin/get/<str:admin_id>',views.GetAdminGroup.as_view(),name='get_admin_group'),
]