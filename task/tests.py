from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from account.tests import AuthCreateUserMixin
from . import models



class GroupTest(AuthCreateUserMixin,APITestCase):

    def authenticate(self,user):
        self.authenticate_user(user)
        return user

    def create_group(self):
        self.authenticate(self.create_user())
        data = {
            'title': 'Test Group'
        }
        req = self.client.post(reverse('task:create_group'), data)
        self.assertEqual(req.status_code, 200)
        return req

    def test_create_group(self):
        self.create_group()


    def test_delete_group(self):
        req = self.create_group()
        self.assertEqual(req.status_code, 200)
        group_id = req.json().get('result').get('id')
        req = self.client.delete(reverse('task:delete_group',args=(group_id,)))
        self.assertEqual(req.status_code,200)


    def test_create_admin_group(self):
        user = self.create_user()
        self.authenticate(user)
        user = self.login(user)
        data = {
            'user':user['id']
        }
        req = self.client.post(reverse('task:create_admin_group'),data)
        self.assertEqual(req.status_code, 200)


    def test_add_admin_to_group(self):
        group = self.create_group()
        group_id = group.json().get('result').get('id')
        user = self.create_user()
        self.authenticate(user)
        user = self.login(user)
        data = {
            'user': user['id']
        }
        req = self.client.post(reverse('task:create_admin_group'), data)
        data = {
            'admins':[
                req.json()['result']['id']
            ]
        }
        req = self.client.put(reverse('task:add_admin_to_group', args=(group_id,)),data)
        self.assertEqual(req.status_code, 200)
