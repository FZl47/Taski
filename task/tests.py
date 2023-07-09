import datetime
import requests
import io
from django.urls import reverse
from django.core.files.images import ImageFile
from rest_framework.test import APITestCase
from core.utils import get_datetime
from account.tests import AuthCreateUserMixin


class TaskTest(AuthCreateUserMixin, APITestCase):
    _GROUP = None
    _TASK = None

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

    def test_task_create(self):
        if self._TASK is None:
            self.authenticate_user(self.create_user())
            group_id = self.create_group().json()['data']['id']
            req = self.client.get(reverse('account:users_group', args=(group_id,)))
            self.assertEqual(req.status_code, 200)
            user_id = req.json()['data'][0]['id']
            data = {
                'title': 'Task Test',
                'user': user_id
            }
            req = self.client.post(reverse('task:task_create', args=(group_id,)), data=data)
            self.assertEqual(req.status_code, 200)
            self._TASK = req
        return self._TASK

    def test_task_update(self):
        task_id = self.test_task_create().json()['data']['id']
        group_id = self.create_group().json()['data']['id']
        data = {
            'title': 'title task updated !',
            'timeleft': get_datetime() + datetime.timedelta(minutes=10),
            'label': 'label updated !',
            'description': 'Description updated !'
        }
        req = self.client.put(reverse('task:task_update', args=(group_id, task_id)), data=data)
        self.assertEqual(req.status_code, 200)
        return req

    def test_task_list(self):
        self.test_task_create()
        self.authenticate_user(self.create_user())
        group_id = self.create_group().json()['data']['id']
        # order by "latest"
        req = self.client.get(reverse('task:task_list', args=(group_id,)) + '?order_by=latest')
        self.assertEqual(req.status_code, 200)
        # order by "expire_date_asc | expire date closer"
        req = self.client.get(reverse('task:task_list', args=(group_id,)) + '?order_by=expire_date_asc')
        self.assertEqual(req.status_code, 200)
        return req

    def test_task_get(self):
        self.test_task_create()
        self.authenticate_user(self.create_user())
        group_id = self.create_group().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        req = self.client.get(reverse('task:task_retrieve', args=(group_id, task_id)))
        self.assertEqual(req.status_code, 200)
        return req

    def test_task_delete(self):
        task_id = self.test_task_create().json()['data']['id']
        group_id = self.create_group().json()['data']['id']
        req = self.client.delete(reverse('task:task_delete', args=(group_id, task_id)))
        self.assertEqual(req.status_code, 200)

    def test_task_file_create(self):
        self.test_task_create()
        self.authenticate_user(self.create_user())
        group_id = self.create_group().json()['data']['id']
        # tasks user
        req = self.client.get(reverse('task:task_list', args=(group_id,)))
        task_user = req.json()['data']
        if task_user:
            task_user = task_user[0]
        file_raw = requests.get('https://robouav.org/wp-content/uploads/2017/10/python-logo.png').content
        file = ImageFile(io.BytesIO(file_raw), name='file.png')
        data = {
            'file': file,
            'task': task_user['id']
        }
        req = self.client.post(reverse('task:task_file_create', args=(group_id,)), data=data)
        self.assertEqual(req.status_code, 200)
        return req

    def test_task_file_update(self):
        group_id = self.create_group().json()['data']['id']
        task_file_id = self.test_task_file_create().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        file_raw = requests.get(
            'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/640px-Django_logo.svg.png').content
        file = ImageFile(io.BytesIO(file_raw), name='file_new.png')
        data = {
            'file': file,
            'task': task_id
        }
        req = self.client.put(reverse('task:task_file_update', args=(group_id, task_file_id)), data=data)
        self.assertEqual(req.status_code, 200)

    def test_task_file_get(self):
        group_id = self.create_group().json()['data']['id']
        task_file_id = self.test_task_file_create().json()['data']['id']
        req = self.client.get(reverse('task:task_file_retrieve', args=(group_id, task_file_id)))
        self.assertEqual(req.status_code, 200)

    def test_task_file_delete(self):
        group_id = self.create_group().json()['data']['id']
        task_file_id = self.test_task_file_create().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        data = {
            'task': task_id
        }
        req = self.client.delete(reverse('task:task_file_delete', args=(group_id, task_file_id)), data=data)
        self.assertEqual(req.status_code, 200)

    # TaskResponse

    def test_task_response_create(self):
        group_id = self.create_group().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        data = {
            'content': 'test content',
            'task': task_id
        }
        req = self.client.post(reverse('task:task_response_create', args=(group_id,)), data=data)
        self.assertEqual(req.status_code, 200)
        return req

    def test_task_response_update(self):
        group_id = self.create_group().json()['data']['id']
        task_response_id = self.test_task_response_create().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        data = {
            'content': 'content updated !',
            'task': task_id
        }
        req = self.client.put(reverse('task:task_response_update', args=(group_id, task_response_id)), data=data)
        self.assertEqual(req.status_code, 200)

    def test_task_response_get(self):
        group_id = self.create_group().json()['data']['id']
        task_response_id = self.test_task_response_create().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        data = {
            'task': task_id
        }
        req = self.client.get(reverse('task:task_response_retrieve', args=(group_id, task_response_id)), data=data)
        self.assertEqual(req.status_code, 200)

    def test_task_response_delete(self):
        group_id = self.create_group().json()['data']['id']
        task_response_id = self.test_task_response_create().json()['data']['id']
        task_id = self.test_task_create().json()['data']['id']
        data = {
            'task': task_id
        }
        req = self.client.delete(reverse('task:task_response_delete', args=(group_id, task_response_id)), data=data)
        self.assertEqual(req.status_code, 200)
