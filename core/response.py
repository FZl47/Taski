from rest_framework.response import Response as _Response


def Response(data,errors=[],status=200,*args):
    return _Response({
        "data":data,
        "errors":errors,
        "status":status
    },status=status,*args)