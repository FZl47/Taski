from . import serializers


TaskResponse = {
    'tags': ['Task'],
    'methods': {
        'post': {
            'title': 'Create Task Response',
            'description': 'create task response',
            'request_body': serializers.TaskResponse.CreateRequestBody,
            'responses': {
                200: serializers.TaskResponse.Create
            },
        },
        'put': {
            'title': 'Update Task Response',
            'description': 'update task response',
            'request_body': serializers.TaskResponse.UpdateRequestBody,
            'responses': {
                200: serializers.TaskResponse.Update
            },
        },
        'get': {
            'title': 'Get Task Response',
            'description': 'get task response',
            'responses': {
                200: serializers.TaskResponse.Get
            },
        },
        'delete': {
            'title': 'Delete Task Response',
            'description': 'delete task response',
            'request_body':serializers.TaskResponse.DeleteRequestBody,
            'responses': {
                200: serializers.TaskResponse.Delete
            },
        },
    }
}
