from django.test import TestCase
from django.conf import settings
from core import redis_py


class TestThirdPartyService(TestCase):

    def test_redis(self):
        r = redis_py.test_conn()
        self.assertEqual(r, True, 'Redis service is not running')
