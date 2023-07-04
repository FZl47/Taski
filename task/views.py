from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from core.swagger.views import SwaggerMixin
from core.response import Response
from core.views import BaseView
from account import permissions as permissions_account
from . import serializers, models, swagger


class Task(BaseView):
    VIEW_NAMES = ('Create', 'Update', 'Retrieve', 'List', 'Delete')
    SWAGGER = swagger.Task
    permission_classes_additional = (permissions_account.IsOwnerOrAdminGroup,)

    class Create(APIView):
        def post(self, request, group_id):
            data = request.data.copy()  # add group value field
            data.update({
                'group': group_id,
                'created_by': request.admin.id
            })
            s = serializers.Task.CreateRequestBody(data=data)
            s.is_valid()
            s.save()
            return Response(s.data)

    class Update(APIView):
        def put(self, request, group_id, task_id):
            obj = models.Task.get_obj(id=task_id, group_id=group_id, created_by=request.admin)
            s = serializers.Task.UpdateRequestBody(instance=obj, data=request.data)
            s.is_valid()
            obj = s.update(obj, s.validated_data)
            return Response(serializers.Task.Update(obj).data)

    class List(APIView):
        use_child_permission = True
        permission_classes_additional = (permissions_account.IsMemberShip,)

        def get(self, request, group_id):
            group = request.group
            user = request.user
            tasks = user.task_set.filter(group__id__in=[group.id])
            is_completed_param = request.query_params.get('is_completed', 'all')
            match is_completed_param:
                case True:
                    tasks.filter(is_completed=True)
                case False:
                    tasks.filter(is_completed=False)
                case _:
                    # default all tasks
                    pass
            sort_by = request.query_params.get('sort_by', 'latest')
            match sort_by:
                case 'latest':
                    tasks = tasks.order_by('-id')
                case 'oldest':
                    tasks = tasks.order_by('id')
                case 'expire_date_desc':
                    tasks = tasks.order_by('-timeleft')
                case 'expire_date_asc':
                    tasks = tasks.order_by('timeleft')

            return Response(serializers.Task.Get(tasks, many=True).data)

    class Retrieve(APIView):
        use_child_permission = True
        permission_classes_additional = (permissions_account.IsMemberShip,)

        def get(self, request, group_id, task_id):
            obj = models.Task.get_obj(id=task_id, group_id=group_id)
            return Response(serializers.Task.Get(obj).data)

    class Delete(APIView):
        def delete(self, request, group_id, task_id):
            data = {
                'group': group_id,
            }
            s = serializers.Task.DeleteRequestBody(data=data)
            s.is_valid()
            data = s.validated_data
            obj = models.Task.get_obj(id=task_id, group=data['group'], created_by=request.admin)
            response = serializers.Task.Delete(obj).data
            obj.delete()
            return Response(response)


class TaskFile(BaseView):
    VIEW_NAMES = ('Create', 'Update', 'Retrieve', 'Delete')
    SWAGGER = swagger.TaskFile
    permission_classes_additional = (permissions_account.IsOwnerOrAdminGroup,)
    parser_classes = (MultiPartParser,)

    class Create(APIView):

        def post(self, request, group_id):
            s = serializers.TaskFile.CreateRequestBody(data=request.data)
            s.is_valid()
            obj = s.save()
            return Response(serializers.TaskFile.Create(obj).data)

    class Update(APIView):

        def put(self, request, group_id, task_file_id):
            s = serializers.TaskFile.UpdateRequestBody(data=request.data)
            s.is_valid()
            data = s.validated_data
            # Only admin who created task can update task file
            obj = models.TaskFile.get_obj(id=task_file_id, task=data['task'], task__group__id=group_id,
                                          task__created_by=request.admin)
            s.update(obj, s.validated_data)
            return Response(serializers.TaskFile.Update(obj).data)

    class Retrieve(APIView):
        use_child_permission = True
        permission_classes_additional = (permissions_account.IsMemberShip,)

        def get(self, request, group_id, task_file_id):
            obj = models.TaskFile.get_obj(id=task_file_id, task__group__id=group_id)
            return Response(serializers.TaskFile.Get(obj).data)

    class Delete(APIView):
        def delete(self, request, group_id, task_file_id):
            s = serializers.TaskFile.DeleteRequestBody(data=request.data)
            s.is_valid()
            # Only admin who created task can delete task file
            data = s.validated_data
            obj = models.TaskFile.get_obj(id=task_file_id, task=data['task'],
                                          task__group__id=group_id, task__created_by=request.admin)
            response = serializers.TaskFile.Delete(obj).data
            obj.delete()
            return Response(response)


class TaskResponse(BaseView, SwaggerMixin):
    VIEW_NAMES = ('Create', 'Update', 'Retrieve', 'Delete')
    SWAGGER = swagger.TaskResponse
    permission_classes_additional = (permissions_account.IsMemberShip,)

    class Create(APIView):
        def post(self, request, group_id):
            s = serializers.TaskResponse.CreateRequestBody(data=request.data)
            s.is_valid()
            obj = s.save()
            return Response(serializers.TaskResponse.Create(obj).data)

    class Update(APIView):
        def put(self, request, group_id, task_response_id):
            s = serializers.TaskResponse.UpdateRequestBody(data=request.data)
            s.is_valid()
            data = s.validated_data
            obj = models.TaskResponse.get_obj(id=task_response_id, task=data['task'],
                                              task__group__id=group_id, task__user=request.user)
            s.update(obj, s.validated_data)
            return Response(serializers.TaskResponse.Update(obj).data)

    class Retrieve(APIView):
        def get(self, request, group_id, task_response_id):
            obj = models.TaskResponse.get_obj(id=task_response_id,
                                              task__group__id=group_id)
            return Response(serializers.TaskResponse.Get(obj).data)

    class Delete(APIView):
        def delete(self, request, group_id, task_response_id):
            s = serializers.TaskResponse.DeleteRequestBody(data=request.data)
            s.is_valid()
            data = s.validated_data
            # Only user who created task response can delete it
            obj = models.TaskResponse.get_obj(id=task_response_id, task=data['task'],
                                              task__group__id=group_id, task__user=request.user)
            response = serializers.TaskResponse.Delete(obj).data
            obj.delete()
            return Response(response)
