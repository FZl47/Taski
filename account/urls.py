from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


app_name = 'account'
urlpatterns = [
    # User
    path('user/register',views.User.Create.as_view(),name='register'),
    path('user/login',views.User.Login.as_view(),name='login'),
    path('user/update',views.User.UpdateUser.as_view(),name='update_user'),
    path('user/reset-password',views.User.ResetPassword.as_view(),name='reset_password'),
    path('user/reset-password-code',views.User.ResetPasswordCode.as_view(),name='reset_password_code'),
    path('user/token/refresh',views.User.UpdateLogin.as_view(),name='update_login'),
    path('user/delete',views.User.Delete.as_view(),name='delete_user'),
    path('user/groups',views.User.GroupList.as_view(),name='groups_list_user'),

    # Group
    path('group/create',views.Group.Create.as_view(),name='create_group'),
    path('groups/<uuid:group_id>',views.Group.Retrieve.as_view(),name='retrieve_group'),
    path('groups/<uuid:group_id>/delete',views.Group.Delete.as_view(),name='delete_group'),

    # Group User
    path('groups/<uuid:group_id>/user/add/request',views.GroupUser.RequestAddUser.as_view(),name='request_add_group_user'),
    path('group/request/accept/<uuid:token>',views.GroupUser.AcceptRequestJoin.as_view(),name='accept_request_join_group_user'),
    path('groups/<uuid:group_id>/users', views.GroupUser.List.as_view(), name='users_group'),
    path('groups/<uuid:group_id>/users/<uuid:user_id>/delete',views.GroupUser.Kick.as_view(),name='kick_group_user'),

    # Group Admin
    path('groups/<uuid:group_id>/admin/create',views.GroupAdmin.Create.as_view(),name='create_group_admin'),
    path('groups/<uuid:group_id>/admins',views.GroupAdmin.List.as_view(),name='group_admins'),
    path('groups/<uuid:group_id>/admins/<uuid:admin_id>/delete',views.GroupAdmin.Delete.as_view(),name='kick_group_admin'),
]


