from django.contrib.auth.models import User
from django.test import TestCase
from ..forms import UserRegistrationForm, AddressRegistrationForm

class RegistrationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_user_registration_form(self):
        form = UserRegistrationForm(data={
            'username': 'testuser2',
            'first_name': 'test',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
        form.save()
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)
    
    def test_address_registration_form(self):
        form = AddressRegistrationForm(data={
            'street': 'test street 123'
        })
        self.assertTrue(form.is_valid())
        address = form.save(commit=False)
        address.user = self.user
        address.save()
        self.assertTrue(self.user.address_set.exists())