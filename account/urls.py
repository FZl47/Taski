from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


app_name = 'account'
urlpatterns = [
    # User
    path('user/register',views.Register.as_view(),name='register'),
    path('user/login',views.Login.as_view(),name='login'),
    path('user/update',views.UserUpdate.as_view(),name='update_user'),
    path('user/reset-password',views.ResetPassword.as_view(),name='reset_password'),
    path('user/reset-password-code',views.ResetPasswordCode.as_view(),name='reset_password_code'),
    path('user/delete',views.UserDelete.as_view(),name='delete_user'),
    path('user/token/refresh',views.AccessToken.as_view(),name='access_token'),


    # Group
    path('group/create',views.CreateGroup.as_view(),name='create_group'),
    path('group/<uuid:group_id>/delete',views.DeleteGroup.as_view(),name='delete_group'),

    # Group User
    path('group/<uuid:group_id>/users',views.GroupUsers.as_view(),name='group_users'),
    path('group/<uuid:group_id>/users/add/request',views.RequestAddUserToGroup.as_view(),name='request_add_user_group'),
    path('group/request/accept/<uuid:token>',views.AcceptRequestGroupJoin.as_view(),name='accept_request_group_join'),
    path('group/<uuid:group_id>/users/<uuid:user_id>/delete',views.DeleteGroupUser.as_view(),name='group_user_delete'),
    path('group/all',views.GroupList.as_view(),name='group_list'),

    # Admin
    path('group/<uuid:group_id>/admins/create',views.CreateAdminGroup.as_view(),name='create_admin_group'),
    # path('group/<uuid:group_id>/admins/add',views.AddAdminToGroup.as_view(),name='add_admin_to_group'),
    path('group/<uuid:group_id>/admins/<uuid:admin_id>/delete',views.DeleteGroupAdmin.as_view(),name='group_admin_delete'),
    path('group/<uuid:group_id>/admins',views.GroupAdmins.as_view(),name='group_admins'),
]


