from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from ..views import *
from ..forms import AddressRegistrationForm, UserRegistrationForm

class UserRegistrationTest(TestCase):
    
    def setUp(self):
        self.user_data = {
            'username': 'test',
            'first_name': 'test',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
        }
        self.address_data = {
            'street': 'test street 123'
        }

    def test_forms_rendered_in_template(self):
        response = self.client.get(reverse('user:register'))
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['user_form'], UserRegistrationForm)
        self.assertIsInstance(response.context['address_form'], AddressRegistrationForm)

    def test_register_require_both_forms_valid(self):
        data = dict(self.user_data, **self.address_data)
        response = self.client.post(reverse('user:register'), data)
        self.assertEqual(response.status_code, 200)

    def test_cannot_register_without_address(self):
        data = self.user_data
        response = self.client.post(reverse('user:register'), data)
        self.assertFormError(response, 'address_form', 'street', 'This field is required.')

    def test_user_passwords_have_to_match(self):
        data = {
            'username': 'test',
            'first_name': 'test',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password',
        }
        user_form = UserRegistrationForm(data=data)
        self.assertFalse(user_form.is_valid())


class UserProfileTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('test')
        self.user.save()

    def test_profile_render_correct_template(self):
        self.client.login(username='testuser', password='test')
        response = self.client.get(reverse('user:profile'))
        self.assertTemplateUsed(response, 'user/profile.html')

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