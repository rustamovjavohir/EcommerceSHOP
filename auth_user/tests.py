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

#
# class Account(APITestCase):
#     def setUp(self):
#         # image = io.BytesIO()
#         # Image.new('RGB', (400, 200)).save(image, 'JPEG')
#         # image.seek(0)
#         # image_file = SimpleUploadedFile('image.jpg', image.getvalue())
#
#         self.url = reverse('register')
#         self.data = {
#             "first_name": 'Javohir',
#             "last_name": 'Rustamov',
#             "password": '123',
#             "username": 'username',
#             "email": 'user@gmail.com',
#             "data_of_birth": '2000-05-27',
#             # "profile_image": image_file
#         }
#
#     def test_create_account(self):
#         # print(resolve(self.url))
#         response = self.client.post(self.url, data=self.data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         # self.assertEqual(User.objects.filter(username='username').first().profile_image, 'image.jpg')
#         self.assertEqual(User.objects.filter(username='username').first().username, 'username')

#
# class UserLoginTest(APITestCase):
#
#     def setUp(self):
#         self.url = reverse('login')
#         self.data = {
#             "username": "username",
#             "password": "password"
#         }
#         # user = User(username='username', password='password').save()
#         user = User.objects.create_user(username='username', password='password')
#
#     def test_login_user(self):
#         response = self.client.post(self.url, data=self.data, format='multipart')
#         # import pdb
#         # pdb.set_trace()   # natijani consolda korish
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class LogOutTest(APITestCase):
#
#     def setUp(self):
#         self.url = reverse('logout')
#
#     def test_log_out(self):
#         response = self.client.get(self.url,)
