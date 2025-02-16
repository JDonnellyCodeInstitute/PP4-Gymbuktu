from django.test import TestCase
from django.contrib.auth.models import User
from classes.views import staff_required


class TestStaffRequired(TestCase):

    def setUp(self):
        """Set up test users."""
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@test.com",
            password="TestPass123!"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="SuperPass123!"
        )

        self.regular_user = User.objects.create_user(
            username="regular",
            email="regular@test.com",
            password="TestPass123!"
        )

    def test_staff_user_has_access(self):
        """Test that a staff user passes the `staff_required` check."""
        self.assertTrue(staff_required(self.staff_user))
