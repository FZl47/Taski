from django.urls import path
from . import views

app_name = 'task'
urlpatterns = [
    path('task/<uuid:group_id>/all', views.TaskList.as_view(), name='task_list'),
    path('task/<uuid:group_id>/create', views.CreateTask.as_view(), name='create_task'),
    path('task/file/<uuid:group_id>/create', views.CreateTaskFile.as_view(), name='create_task_file'),
]