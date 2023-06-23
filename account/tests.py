import os
import urllib.request
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from core import utils


class AuthCreateUserMixin:
    user = None
    def create_user(self):
        if self.user == None:
            data = {
                'first_name': 'Fazel',
                'last_name': 'Momeni',
                'email': 'test@gmail.com',
                'password': 'ThisIsTestPassword'
            }
            req = self.client.post(reverse('account:register'), data)
            self.assertEqual(req.status_code, 200)
            req = req.json()
            data = req['data']
            self.user = data
            return data
        else:
            return self.user

    def authenticate_user(self, user):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user['access']}")

    def login(self,user):
        data = {
            'username': 'test@gmail.com',
            'password': 'ThisIsTestPassword'
        }
        req = self.client.post(reverse('account:login'), data)
        self.assertEqual(req.status_code, 200)
        req = req.json()
        return req['data']


class AccountTest(AuthCreateUserMixin,APITestCase):

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
        user = self.create_user()
        refresh_token = user['refresh']
        data = {
            'refresh': refresh_token
        }
        req = self.client.post(reverse('account:access_token'), data)
        self.assertEqual(req.status_code, 200)


    def test_update_user(self):
        user = self.create_user()
        self.authenticate_user(user)
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
        # user = self.create_user()
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
        # user = self.create_user()
        # data = {
        #     'email': 'test@gmail.com',
        #     'code':'...',
        #     'new_password':'NewPassword'
        # }
        # req = self.client.post(reverse('account:reset_password_code'), data)
        # self.assertEqual(req.status_code, 200)
        pass


    def test_delete_user(self):
        user = self.create_user()
        self.authenticate_user(user)
        data = {
            'password': 'ThisIsTestPassword'
        }
        req = self.client.delete(reverse('account:delete_user'), data)
        self.assertEqual(req.status_code, 200)




@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class GroupTest(AuthCreateUserMixin,APITestCase):

    def authenticate(self,user):
        self.authenticate_user(user)
        return user

    def create_group(self):
        self.authenticate(self.create_user())
        data = {
            'title': 'Test Group'
        }
        req = self.client.post(reverse('account:create_group'), data)
        self.assertEqual(req.status_code, 200)
        return req

    def test_create_group(self):
        self.create_group()

    def test_delete_group(self):
        req = self.create_group()
        group_id = req.json().get('data').get('id')
        req = self.client.delete(reverse('account:delete_group',args=(group_id,)))
        self.assertEqual(req.status_code,200)

    def test_create_admin_group(self):
        user = self.create_user()
        self.authenticate(user)
        user = self.login(user)
        data = {
            'user':user['id']
        }
        req = self.create_group()
        group_id = req.json().get('data').get('id')
        req = self.client.post(reverse('account:create_admin_group',args=(group_id,)),data)
        self.assertEqual(req.status_code, 200)

    # def test_add_admin_to_group(self):
    #     group = self.create_group()
    #     group_id = group.json().get('data').get('id')
    #     user = self.create_user()
    #     self.authenticate(user)
    #     user = self.login(user)
    #     data = {
    #         'user': user['id']
    #     }
    #     req = self.client.post(reverse('account:create_admin_group'), data)
    #     data = {
    #         'admins':[
    #             req.json()['data']['id']
    #         ]
    #     }
    #     req = self.client.put(reverse('account:add_admin_to_group', args=(group_id,)),data)
    #     self.assertEqual(req.status_code, 200)


    def test_add_user_to_group(self):
        member_user = self.login(self.create_user())
        group_id = self.create_group().json()['data']['id']
        owner_user = self.login(self.user)
        data = {
            'email':member_user['email']
        }
        req = self.client.post(reverse('account:request_add_user_group',args=(group_id,)), data)
        self.assertEqual(req.status_code, 200)