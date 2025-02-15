from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from accounts.models import EmailVerification


class TestSignupView(TestCase):

    def setUp(self):
        """Set up test client and default user."""
        self.client = Client()
        self.signup_url = reverse("signup")

        # Create an existing user for duplicate username tests
        self.existing_user = User.objects.create_user(
            username="ExistingUser",
            email="existing@gmail.com",
            password="TestPassword1!"
        )

    def test_successful_signup(self):
        """Test a successful signup creates a user,
        sends an email, and redirects."""
        response = self.client.post(self.signup_url, {
            "username": "NewUser",
            "email": "newuser@gmail.com",
            "password1": "StrongPassword1!",
            "password2": "StrongPassword1!",
        })

        # User should be created
        self.assertTrue(User.objects.filter(username="NewUser").exists())

        # Should redirect to check email page
        self.assertRedirects(response, reverse("check_email"))

        # Email should be sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Verify Your Account", mail.outbox[0].subject)

        # Verification token should be created
        self.assertTrue(EmailVerification.objects.filter(
            user__username="NewUser").exists())
