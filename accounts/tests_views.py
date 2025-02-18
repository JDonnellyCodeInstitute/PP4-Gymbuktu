from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core import mail
from accounts.models import EmailVerification
from classes.models import Booking, Class, Instructor, Facilitie
from django.utils.timezone import now
import uuid


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

    def test_signup_fails_if_username_taken(self):
        """Test that signing up with an existing username shows an error."""
        response = self.client.post(self.signup_url, {
            "username": "ExistingUser",  # Username already taken in setup
            "email": "newuser@gmail.com",
            "password1": "StrongPassword1!",
            "password2": "StrongPassword1!",
        })

        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

        # Error message should be in the response
        self.assertContains(response, "This username is already taken.")

    def test_signup_fails_if_password_too_weak(self):
        """Test that a weak password shows an error message."""
        response = self.client.post(self.signup_url, {
            "username": "NewUser",
            "email": "newuser@gmail.com",
            "password1": "1234",
            "password2": "1234",
        })

        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

        # Error message should be in the response
        self.assertContains(
            response, "Your password does not meet the security requirements")

        # User should NOT be created
        self.assertFalse(User.objects.filter(username="NewUser").exists())

    def test_signup_fails_if_passwords_dont_match(self):
        """Test that mismatched passwords fail validation."""
        response = self.client.post(self.signup_url, {
            "username": "NewUser",
            "email": "newuser@gmail.com",
            "password1": "StrongPassword1!",
            "password2": "WrongPassword1!",
        })

        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

        # Error message should be in the response
        self.assertContains(
            response, "Password2: The two password fields didn’t match.")

        # User should NOT be created
        self.assertFalse(User.objects.filter(username="NewUser").exists())

    def test_signup_fails_if_missing_fields(self):
        """Test that signup fails when required fields are missing."""
        response = self.client.post(self.signup_url, {
            "username": "",
            "email": "newuser@gmail.com",
            "password1": "StrongPassword1!",
            "password2": "StrongPassword1!",
        })

        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

        # Error message should be in the response
        self.assertContains(response, "This field is required.")

        # User should NOT be created
        self.assertFalse(User.objects.filter(
            email="newuser@gmail.com").exists())


class TestLoginView(TestCase):

    def setUp(self):
        """Set up test client and create test users."""
        self.client = Client()
        self.login_url = reverse("login")

        # Create an active user for successful login
        self.active_user = User.objects.create_user(
            username="ActiveUser",
            email="activeuser@gmail.com",
            password="TestPassword1!"
        )

        # Create an inactive (unverified) user
        self.inactive_user = User.objects.create_user(
            username="InactiveUser",
            email="inactiveuser@gmail.com",
            password="TestPassword1!"
        )
        self.inactive_user.is_active = False
        self.inactive_user.save()

    def test_successful_login(self):
        """Test successful login redirects to
        profile and shows success message."""
        response = self.client.post(self.login_url, {
            "username": "ActiveUser",
            "password": "TestPassword1!",
        })

        # User should be redirected to profile
        self.assertRedirects(response, reverse("profile"))

        # Check that success message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "Welcome back, ActiveUser!" in msg.message for msg in messages))

    def test_login_fails_with_invalid_credentials(self):
        """Test that login fails with incorrect username/password."""
        response = self.client.post(self.login_url, {
            "username": "WrongUser",
            "password": "WrongPassword!",
        })

        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

        # Check that error message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "Username or password is unrecognised." in msg.message
            for msg in messages
        ))

    def test_login_fails_for_unverified_user(self):
        """Test that login fails for an unverified (inactive) user."""
        response = self.client.post(self.login_url, {
            "username": "InactiveUser",
            "password": "TestPassword1!",
        })

        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

        # Check that error message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "Username or password is unrecognised." in msg.message
            for msg in messages
        ))

    def test_login_fails_with_empty_fields(self):
        """Test that login fails when fields are left empty."""
        response = self.client.post(self.login_url, {
            "username": "",
            "password": "",
        })

        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

        # Check that error message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "Username or password is unrecognised." in msg.message
            for msg in messages
        ))


class TestVerifyEmailView(TestCase):

    def setUp(self):
        """Set up test client and create a user with verification token."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="TestUser",
            email="testuser@gmail.com",
            password="TestPassword1!",
            is_active=False  # User should start inactive
        )

        # Create a verification token
        self.token_obj = EmailVerification.objects.create(
            user=self.user,
            token=uuid.uuid4(),
            is_verified=False  # Starts as unverified
        )
        self.verify_url = reverse(
            "verify_email", args=[str(self.token_obj.token)])

    def test_successful_verification(self):
        """Test that a valid token activates
        the user and redirects to login."""
        response = self.client.get(self.verify_url)

        # Check that user is now active
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        # Check that token is marked as verified
        self.token_obj.refresh_from_db()
        self.assertTrue(self.token_obj.is_verified)

        # Check success message appears
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "Your account has been verified. You can now log in."
            in msg.message for msg in messages
        ))

        # Should redirect to login page
        self.assertRedirects(response, reverse("login"))

    def test_already_verified_token(self):
        """Test that visiting an already verified
        token shows 'already verified' page."""
        # Mark token as verified and activate user
        self.token_obj.is_verified = True
        self.token_obj.save()

        self.user.is_active = True
        self.user.save()

        response = self.client.get(self.verify_url)

        # Should render the already verified template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/already_verified.html")

        # User should still be active
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_invalid_token(self):
        """Test that an invalid token returns a 404 error."""
        invalid_url = reverse("verify_email", args=[str(uuid.uuid4())])
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, 404)


class TestCheckEmailView(TestCase):

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.check_email_url = reverse("check_email")

    def test_check_email_renders_correct_template(self):
        """Test that check_email view loads and uses the correct template."""
        response = self.client.get(self.check_email_url)

        # The page should load successfully
        self.assertEqual(response.status_code, 200)

        # It should use the correct template
        self.assertTemplateUsed(response, "accounts/check_email.html")


class TestAlreadyVerifiedView(TestCase):

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.already_verified_url = reverse("already_verified")

    def test_already_verified_renders_correct_template(self):
        """Test that already_verified view
        loads and uses the correct template."""
        response = self.client.get(self.already_verified_url)

        # The page should load successfully
        self.assertEqual(response.status_code, 200)

        # It should use the correct template
        self.assertTemplateUsed(response, "accounts/already_verified.html")


class TestProfileView(TestCase):

    def setUp(self):
        """Set up test client, user, instructor, and sample bookings."""
        self.client = Client()
        self.profile_url = reverse("profile")

        # Create test user
        self.user = User.objects.create_user(
            username="TestUser",
            email="testuser@gmail.com",
            password="TestPassword1!"
        )

        # Create an instructor
        self.instructor = Instructor.objects.create(name="Keith")

        # Create a test facility
        self.facility = Facilitie.objects.create(
            name="Reception",
            max_capacity=10
        )

        # Set class times to avoid overlap
        start_time_current = now().replace(hour=23, minute=30)
        end_time_current = now().replace(hour=23, minute=59)

        start_time_past = now().replace(hour=22, minute=0)
        end_time_past = now().replace(hour=22, minute=30)

        # Create a test class for current bookings
        self.test_class = Class.objects.create(
            name="Test Class",
            start_time=start_time_current,
            end_time=end_time_current,
            instructor=self.instructor,
            facility=self.facility
        )

        # Create a separate test class for past bookings
        self.past_test_class = Class.objects.create(
            name="Past Test Class",
            start_time=start_time_past,
            end_time=end_time_past,
            instructor=self.instructor,
            facility=self.facility
        )

        # Create bookings for the user
        self.current_booking = Booking.objects.create(
            user=self.user,
            gym_class=self.test_class,
            class_status=0
        )

        self.past_booking = Booking.objects.create(
            user=self.user,
            gym_class=self.past_test_class,
            class_status=2
        )

    def test_redirects_if_not_logged_in(self):
        """Test that unauthenticated users are redirected to the login page."""
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.profile_url}"
        )

    def test_profile_page_loads_for_logged_in_user(self):
        """Test that the profile page loads
        successfully for an authenticated user."""
        self.client.login(username="TestUser", password="TestPassword1!")
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertContains(response, "TestUser")

    def test_current_bookings_displayed_in_profile(self):
        """Test that current bookings appear on the profile page."""
        self.client.login(username="TestUser", password="TestPassword1!")
        response = self.client.get(self.profile_url)

        self.assertContains(response, "Test Class")

    def test_past_bookings_displayed_in_profile(self):
        """Test that past bookings appear on the profile page."""
        self.client.login(username="TestUser", password="TestPassword1!")
        response = self.client.get(self.profile_url)

        self.assertContains(response, "Past Test Class")


class TestAutoLogoutView(TestCase):

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.login_url = reverse("login")
        self.auto_logout_url = reverse("auto_logout")

        # Create test user
        self.user = User.objects.create_user(
            username="TestUser",
            email="testuser@gmail.com",
            password="TestPassword1!"
        )

    def test_auto_logout_redirects_to_login(self):
        """Test that auto_logout logs the user out and redirects to login."""
        self.client.login(username="TestUser", password="TestPassword1!")

        response = self.client.get(self.auto_logout_url)

        self.assertRedirects(response, self.login_url)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_auto_logout_shows_warning_message(self):
        """Test that auto_logout displays a logout warning message."""
        self.client.login(username="TestUser", password="TestPassword1!")

        response = self.client.get(self.auto_logout_url, follow=True)

        messages = list(response.context["messages"])
        self.assertTrue(any(
            "You have been logged out due to inactivity." in msg.message
            for msg in messages
        ))
