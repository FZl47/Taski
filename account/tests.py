import urllib.request
import os
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from core import utils


class AccountTest(APITestCase):

    def create_user(self):
        data = {
            'first_name': 'Fazel',
            'last_name': 'Momeni',
            'email': 'test@gmail.com',
            'password': 'ThisIsTestPassword'
        }
        req = self.client.post(reverse('account:register'), data)
        self.assertEqual(req.status_code, 200)
        req = req.json()
        return req['result']

    def authenticate_user(self, usr):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {usr['access']}")

    def test_create_account(self):
        self.create_user()

    def test_login(self):
        self.create_user()
        data = {
            'username': 'test@gmail.com',
            'password': 'ThisIsTestPassword'
        }
        req = self.client.post(reverse('account:login'), data)
        self.assertEqual(req.status_code, 200)

    def test_update_access_token(self):
        usr = self.create_user()
        refresh_token = usr['refresh']
        data = {
            'refresh': refresh_token
        }
        req = self.client.post(reverse('account:access_token'), data)
        self.assertEqual(req.status_code, 200)

    def test_update_user(self):
        usr = self.create_user()
        self.authenticate_user(usr)
        data = {
            'first_name': 'Fazel updated !',
            'last_name': 'Momeni updated !',
            'last_login': utils.get_datetime_f()
        }
        req = self.client.put(reverse('account:update_user'), data)
        self.assertEqual(req.status_code, 200)


    def test_reset_password(self):
        """
            This test need code sended to email
            so this is useless
        """
        # usr = self.create_user()
        # data = {
        #     'email': 'test@gmail.com'
        # }
        # req = self.client.post(reverse('account:reset_password'), data)
        # self.assertEqual(req.status_code, 200)
        pass


    def test_reset_password_code(self):
        """
            This test need code sended to email
            so this is useless
        """
        # usr = self.create_user()
        # data = {
        #     'email': 'test@gmail.com',
        #     'code':'...',
        #     'new_password':'NewPassword'
        # }
        # req = self.client.post(reverse('account:reset_password_code'), data)
        # self.assertEqual(req.status_code, 200)
        pass


    def test_delete_user(self):
        usr = self.create_user()
        self.authenticate_user(usr)
        data = {
            'password': 'ThisIsTestPassword'
        }
        req = self.client.delete(reverse('account:delete_user'), data)
        self.assertEqual(req.status_code, 200)

