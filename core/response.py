from rest_framework.response import Response as _Response


def Response(result,message=[],status=200,*args):
    return _Response({
        "result":result,
        "messages":message,
        "status":status
    },status=status,*args)