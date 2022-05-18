from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from .models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
import json
import io
from PIL import Image


class Account(APITestCase):
    def setUp(self):

        self.url = reverse('sign_up')
        self.data = {
            "first_name": 'Javohir',
            "last_name": 'Rustamov',
            "password": 'password',
            "username": 'user1',
            "email": 'user1@gmail.com',
            "data_of_birth": '2000-05-27',
            "is_staff": True,
        }

    def test_signUp(self):
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.filter(username='user1').first().username, 'user1')


class UserLoginTest(APITestCase):

    def setUp(self):
        self.url = reverse('token_obtain_pair')
        self.data = {
            "username": "admin",
            "password": "admin"
        }
        user = User.objects.create_user(username='admin', password='admin')

    def test_login_user(self):
        response = self.client.post(self.url, data=self.data, format='json')
        # import pdb
        # pdb.set_trace()   # natijani consolda korish
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#
# class LogOutTest(APITestCase):
#
#     def setUp(self):
#         self.url = reverse('logout')
#
#     def test_log_out(self):
#         response = self.client.get(self.url,)
