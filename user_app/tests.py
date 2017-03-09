from django.test import TestCase, Client
from user_app.models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import hashers
import json


class ApiTestCase(TestCase):
    def setUp(self):
        password = hashers.make_password('anubhav')
        self.user = CustomUser.objects.create(email='anubhav@gmail.com', password=password, first_name='anubhav',
                                         last_name='verma', age=20)
        Token.objects.create(key='authorization_token', user=self.user)

    def test_get_user(self):
        c = Client()
        response = c.get('/api/user/{0}/'.format(self.user.id), **{'HTTP_AUTHORIZATION': 'Token authorization_token'})
        self.assertEqual(response.status_code, 200)
        user = {u'age': 20, u'first_name': u'anubhav', u'last_name': u'verma', u'id': self.user.id, u'email': u'anubhav@gmail.com'}
        self.assertEqual(json.loads(response.content), user)

    def test_login(self):
        c = Client()
        response = c.post('/api/login/', {'email': 'anubhav@gmail.com', 'password': 'anubhav'})
        self.assertEqual(response.status_code, 200)
        token = {u'key': u'authorization_token', u'user': self.user.id}
        self.assertEqual(json.loads(response.content), token)

    def test_add_user(self):
        c = Client()
        user = {'age': 20, 'first_name': 'anubhav', 'last_name': 'verma', 'email': 'anubhavverma@gmail.com',
                'password': 'anubhav'}
        response = c.post('/api/user/', user)
        self.assertEqual(response.status_code, 201)

    def test_logout(self):
        c = Client()
        response = c.get('/api/logout/', **{'HTTP_AUTHORIZATION': 'Token authorization_token'})
        self.assertEqual(response.status_code, 200)

    def test_bad_login(self):
        c = Client()
        response = c.post('/api/login/', {'email': 'anubhav@gmail.com', 'password': 'anubha'})
        self.assertEqual(response.status_code, 401)
