from django.urls import path
from . import views


app_name = 'task'
urlpatterns = [
    # Group
    path('group/create',views.CreateGroup.as_view(),name='create_group'),
    path('group/<str:group_id>/delete',views.DeleteGroup.as_view(),name='delete_group'),
    # Admin
    path('group/admin/create',views.CreateAdminGroup.as_view(),name='create_admin_group'),
    path('group/<str:group_id>/admin/add',views.AddAdminToGroup.as_view(),name='add_admin_to_group'),
    path('group/<str:group_id>/admin/get/<str:admin_id>',views.GetAdminGroup.as_view(),name='get_admin_group'),
]