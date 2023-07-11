from django.urls import path
from . import views

app_name = 'task'
urlpatterns = [
    # Task
    path('<uuid:group_id>/task/create', views.Task.Create.as_view(), name='task_create'),
    path('<uuid:group_id>/tasks/<uuid:task_id>/update', views.Task.Update.as_view(), name='task_update'),
    path('<uuid:group_id>/tasks/<uuid:task_id>', views.Task.Retrieve.as_view(), name='task_retrieve'),
    path('<uuid:group_id>/tasks', views.Task.List.as_view(), name='task_list'),
    path('<uuid:group_id>/tasks/<uuid:task_id>/delete', views.Task.Delete.as_view(), name='task_delete'),

    # Task File
    path('<uuid:group_id>/task/file', views.TaskFile.Create.as_view(), name='task_file_create'),
    path('<uuid:group_id>/task/files/<uuid:task_file_id>/update', views.TaskFile.Update.as_view(), name='task_file_update'),
    path('<uuid:group_id>/task/files/<uuid:task_file_id>', views.TaskFile.Retrieve.as_view(), name='task_file_retrieve'),
    path('<uuid:group_id>/task/files/<uuid:task_file_id>/delete', views.TaskFile.Delete.as_view(), name='task_file_delete'),

    # Task Response
    path('<uuid:group_id>/task/response', views.TaskResponse.Create.as_view(), name='task_response_create'),
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>/update', views.TaskResponse.Update.as_view(), name='task_response_update'),
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>', views.TaskResponse.Retrieve.as_view(), name='task_response_retrieve'),
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>/delete', views.TaskResponse.Delete.as_view(), name='task_response_delete'),

    # Task Response File
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>/file/create', views.TaskResponseFile.Create.as_view(), name='task_response_file_create'),
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>/files/<uuid:task_response_file_id>/update', views.TaskResponseFile.Update.as_view(), name='task_response_file_update'),
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>/files/<uuid:task_response_file_id>', views.TaskResponseFile.Retrieve.as_view(), name='task_response_file_retrieve'),
    path('<uuid:group_id>/task/responses/<uuid:task_response_id>/files/<uuid:task_response_file_id>/delete', views.TaskResponseFile.Delete.as_view(), name='task_response_file_delete'),
]

