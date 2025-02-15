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

    def test_username_is_required(self):
        signup_form = SignUpForm({
            'username': '',
            'email': 'gymbuktu@gmail.com',
            'password1': 'testPassword1!',
            'password2': 'testPassword1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_email_is_required(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': '',
            'password1': 'testPassword1!',
            'password2': 'testPassword1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_password1_is_required(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'gymbuktu@gmail.com',
            'password1': '',
            'password2': 'testPassword1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_password2_is_required(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'gymbuktu@gmail.com',
            'password1': 'testPassword1!',
            'password2': ''
        })
        self.assertFalse(signup_form.is_valid())

    def test_passwords_must_match(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'gymbuktu@gmail.com',
            'password1': 'testPassword1',
            'password2': 'testPassword1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_username_too_long(self):
        long_username = 'T' * 151
        signup_form = SignUpForm({
            'username': long_username,
            'email': 'gymbuktu@gmail.com',
            'password1': 'testPassword1!',
            'password2': 'testPassword1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_password_too_short(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'gymbuktu@gmail.com',
            'password1': 'short1!',
            'password2': 'short1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_invalid_email(self):
        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'invalid-email',
            'password1': 'testPassword1!',
            'password2': 'testPassword1!'
        })
        self.assertFalse(signup_form.is_valid())

    def test_duplicate_email_allowed(self):
        SignUpForm({
            'username': 'User1',
            'email': 'duplicate@gmail.com',
            'password1': 'ValidPass1!',
            'password2': 'ValidPass1!'
        }).save()

        signup_form = SignUpForm({
            'username': 'User2',
            'email': 'duplicate@gmail.com',
            'password1': 'ValidPass1!',
            'password2': 'ValidPass1!'
        })
        self.assertTrue(signup_form.is_valid())

    def test_duplicate_username(self):
        SignUpForm({
            'username': 'TestUser',
            'email': 'unique1@gmail.com',
            'password1': 'ValidPass1!',
            'password2': 'ValidPass1!'
        }).save()

        signup_form = SignUpForm({
            'username': 'TestUser',
            'email': 'unique2@gmail.com',
            'password1': 'ValidPass2!',
            'password2': 'ValidPass2!'
        })
        self.assertFalse(signup_form.is_valid())
