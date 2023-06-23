import requests
import io
from django.urls import reverse
from django.core.files.images import ImageFile
from rest_framework.test import APITestCase
from account.tests import AuthCreateUserMixin


class TaskTest(AuthCreateUserMixin,APITestCase):
    _GROUP = None

    def create_group(self):
        if self._GROUP is None:
            self.authenticate_user(self.create_user())
            data = {
                'title': 'Test Group'
            }
            req = self.client.post(reverse('account:create_group'), data)
            self.assertEqual(req.status_code, 200)
            self._GROUP = req
        return self._GROUP

    def test_task_list(self):
        self.test_task_create()
        self.authenticate_user(self.create_user())
        group_id = self.create_group().json()['data']['id']
        # order by "latest"
        req = self.client.get(reverse('task:task_list',args=(group_id,)) + '?order_by=latest')
        self.assertEqual(req.status_code,200)
        # order by "expire_date_asc | expire date closer"
        req = self.client.get(reverse('task:task_list',args=(group_id,)) + '?order_by=expire_date_asc')
        self.assertEqual(req.status_code, 200)

    def test_task_create(self):
        self.authenticate_user(self.create_user())
        group_id = self.create_group().json()['data']['id']
        req = self.client.get(reverse('account:group_users',args=(group_id,)))
        self.assertEqual(req.status_code,200)
        group_users = list(map(lambda i:i['id'],req.json()['data']))
        data = {
            'title':'Task Test',
            'users':group_users
        }
        req = self.client.post(reverse('task:create_task',args=(group_id,)),data=data)
        self.assertEqual(req.status_code,200)

    # def test_task_file_create(self):
    #     self.test_task_create()
    #     self.authenticate_user(self.create_user())
    #     group_id = self.create_group().json()['data']['id']
    #     # tasks user
    #     req = self.client.get(reverse('task:task_list',args=(group_id,)))
    #     task_user = req.json()['data']
    #     if task_user:
    #         task_user = task_user[0]
    #     file_raw = requests.get('https://secureanycloud.com/wp-content/uploads/sites/33/2018/11/python.png').content
    #     file = ImageFile(io.BytesIO(file_raw), name='file.png')
    #     data = {
    #         'file': file,
    #         'task':task_user['id']
    #     }
    #     req = self.client.post(reverse('task:create_task_file', args=(group_id,)), data=data)
    #     self.assertEqual(req.status_code, 200)





