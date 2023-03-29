from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from account.tests import AuthCreateUserMixin



class GroupTest(AuthCreateUserMixin,APITestCase):

    def authenticate(self):
        user = self.create_user()
        self.authenticate_user(user)
        return user

    def create_group(self):
        self.authenticate()
        data = {
            'title': 'Test Group'
        }
        req = self.client.post(reverse('task:create_group'), data)
        return req

    def test_create_group(self):
        req = self.create_group()
        self.assertEqual(req.status_code, 200)


    def test_delete_group(self):
        req = self.create_group()
        self.assertEqual(req.status_code, 200)
        group_id = req.json().get('result').get('id')
        req = self.client.delete(reverse('task:delete_group',args=(group_id,)))
        self.assertEqual(req.status_code,200)

