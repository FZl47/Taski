from django.http import JsonResponse


def error_404(request, exception=None):
    return JsonResponse({
        "data": [],
        "errors": ['Not found'],
        "status": 404
    },status=404)
