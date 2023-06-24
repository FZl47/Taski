from django.urls import path
from . import views

app_name = 'task'
urlpatterns = [
    path('task/<uuid:group_id>/all', views.TaskList.as_view(), name='task_list'),
    path('task/<uuid:group_id>/create', views.CreateTask.as_view(), name='create_task'),
    path('task/<uuid:group_id>/<uuid:task_id>/update', views.UpdateTask.as_view(), name='update_task'),
    path('task/<uuid:group_id>/<uuid:task_id>/users/update', views.UpdateUsersTask.as_view(), name='update_users_task'),
    path('task/<uuid:group_id>/<uuid:task_id>/delete', views.DeleteTask.as_view(), name='delete_task'),
    path('task/file/<uuid:group_id>/create', views.CreateTaskFile.as_view(), name='create_task_file'),
]