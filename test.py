import datetime
from django_q.tasks import async_task
from django.http import HttpResponse
from core.utils import get_datetime_div


def test_func(x):
    import time
    time.sleep(5)
    print(x)


def test_view(request):
    timeleft = datetime.datetime.strptime('2023-6-28 12:00','%Y-%m-%d %H:%M')
    print(get_datetime_div(datetime.datetime.now(),timeleft, 5))
    async_task(test_func, 'Hi')
    return HttpResponse('OK')
