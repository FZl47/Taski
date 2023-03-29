from django.urls import path
from . import views


app_name = 'task'
urlpatterns = [
    path('group/create',views.CreateGroup.as_view(),name='create_group'),
    path('group/delete/<str:group_id>',views.DeleteGroup.as_view(),name='delete_group'),
]