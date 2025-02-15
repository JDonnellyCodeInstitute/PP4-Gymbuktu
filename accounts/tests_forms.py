from django.test import TestCase
from .forms import SignUpForm, CustomLoginForm


class TestSignUpForm(TestCase):

    def test_form_is_valid(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'gymbuktu@gmail.com',
            'password1': 'testPassword1!',
            'password2': 'testPassword1!'
        })
        self.assertTrue(signup_form.is_valid())
