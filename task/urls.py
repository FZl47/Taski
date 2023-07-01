from django.urls import path
from . import views

app_name = 'task'
urlpatterns = [
    # Task
    path('task/<uuid:group_id>/all', views.TaskList.as_view(), name='task_list'),
    path('task/<uuid:group_id>/create', views.CreateTask.as_view(), name='create_task'),
    path('task/<uuid:group_id>/<uuid:task_id>/update', views.UpdateTask.as_view(), name='update_task'),
    path('task/<uuid:group_id>/<uuid:task_id>/delete', views.DeleteTask.as_view(), name='delete_task'),
    # Task File
    path('task/file/<uuid:group_id>/create', views.CreateTaskFile.as_view(), name='create_task_file'),
    path('task/file/<uuid:group_id>/<uuid:task_id>/<uuid:task_file_id>/get', views.GetTaskFile.as_view(), name='get_task_file'),
    path('task/file/<uuid:group_id>/<uuid:task_id>/<uuid:task_file_id>/update', views.UpdateTaskFile.as_view(), name='update_task_file'),
    path('task/file/<uuid:group_id>/<uuid:task_id>/<uuid:task_file_id>/delete', views.DeleteTaskFile.as_view(), name='delete_task_file'),
    # Task Response
    path('task/response/<uuid:group_id>/<uuid:task_id>/create', views.CreateTaskResponse.as_view(), name='create_task_response'),
    path('task/response/<uuid:group_id>/<uuid:task_id>/<uuid:task_response_id>/update', views.UpdateTaskResponse.as_view(), name='update_task_response'),
    path('task/response/<uuid:group_id>/<uuid:task_id>/<uuid:task_response_id>/get', views.GetTaskResponse.as_view(), name='get_task_response'),
    path('task/response/<uuid:group_id>/<uuid:task_id>/<uuid:task_response_id>/delete', views.DeleteTaskResponse.as_view(), name='delete_task_response'),
    # Task Response File
    # path('task/response/file/<uuid:group_id>/<uuid:task_id>/<uuid:task_response_id>/create', views.CreateTaskResponseFile.as_view(), name='create_task_response_file'),
]