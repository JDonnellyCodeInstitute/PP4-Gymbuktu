from django.test import TestCase
from django.contrib.auth.models import User
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


class TestCustomLoginForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up a user for authentication tests."""
        cls.user = User.objects.create_user(
            username="TestUser",
            email="testuser@gmail.com",
            password="TestPassword1!"
        )

    def test_form_is_valid(self):
        """Test that a valid login form is accepted."""
        login_form = CustomLoginForm(data={
            "username": "TestUser",
            "password": "TestPassword1!"
        })
        self.assertTrue(login_form.is_valid())

    def test_username_is_required(self):
        """Test that the login form fails when username is missing."""
        login_form = CustomLoginForm(data={
            "username": "",
            "password": "TestPassword1!"
        })
        self.assertFalse(login_form.is_valid())

    def test_password_is_required(self):
        """Test that the login form fails when password is missing."""
        login_form = CustomLoginForm(data={
            "username": "TestUser",
            "password": ""
        })
        self.assertFalse(login_form.is_valid())

    def test_invalid_credentials_password(self):
        """Test that an incorrect password is rejected."""
        login_form = CustomLoginForm(data={
            "username": "TestUser",
            "password": "WrongPassword123!"
        })
        self.assertFalse(login_form.is_valid())

    def test_invalid_credentials_username(self):
        """Test that an incorrect username is rejected."""
        login_form = CustomLoginForm(data={
            "username": "WrongTestUser",
            "password": "TestPassword1!"
        })
        self.assertFalse(login_form.is_valid())
