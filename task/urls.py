from django.urls import path
from . import views


app_name = 'task'
urlpatterns = [
    # Group
    path('group/create',views.CreateGroup.as_view(),name='create_group'),
    path('group/<str:group_id>/delete',views.DeleteGroup.as_view(),name='delete_group'),
    # Group User
    path('group/<str:group_id>/users',views.GroupUsers.as_view(),name='group_users'),
    path('group/<str:group_id>/users/add/request',views.AddUserToGroup.as_view(),name='add_user_group'),
    path('group/<str:group_id>/users/<str:user_id>/delete',views.DeleteGroupUser.as_view(),name='group_user_delete'),
    # Admin
    path('group/admin/create',views.CreateAdminGroup.as_view(),name='create_admin_group'),
    path('group/<str:group_id>/admins/add',views.AddAdminToGroup.as_view(),name='add_admin_to_group'),
    path('group/<str:group_id>/admins/<str:admin_id>/delete',views.DeleteGroupAdmin.as_view(),name='group_admin_delete'),
    path('group/<str:group_id>/admins',views.GroupAdmins.as_view(),name='group_admins'),
    # path('group/<str:group_id>/admin/get/<str:admin_id>',views.GetAdminGroup.as_view(),name='get_admin_group'),
]