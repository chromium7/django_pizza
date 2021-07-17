from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..views import *

class UserRegistrationTest(TestCase):
    pass

class UserProfileTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('test')
        self.user.save()

    def test_authenticated_user_access(self):
        self.client.login(username='testuser', password='test')
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_anonymous_access(self):
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 302)

    def test_order_detail_doesnt_exist(self):
        response = self.client.get(reverse('user:order', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)