from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from classes.views import staff_required
from classes.models import Class, Booking, Instructor, Facilitie


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

    def test_superuser_has_access(self):
        """Test that a superuser passes the `staff_required` check."""
        self.assertTrue(staff_required(self.superuser))

    def test_regular_user_denied_access(self):
        """Test that a non-staff, non-superuser
        fails the `staff_required` check."""
        self.assertFalse(staff_required(self.regular_user))


class TestManageClassesView(TestCase):

    def setUp(self):
        """Set up test users, instructors, facilities, and classes."""
        self.client = Client()
        self.manage_classes_url = reverse("manage_classes")

        # Create users
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@test.com",
            password="TestPass123!"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.regular_user = User.objects.create_user(
            username="regular",
            email="regular@test.com",
            password="TestPass123!"
        )

        # Create an instructor and facility
        self.instructor = Instructor.objects.create(name="John Doe")
        self.facility = Facilitie.objects.create(
            name="Main Hall",
            max_capacity=10
        )

        # Create a class
        self.class_date = now().date()
        self.test_class = Class.objects.create(
            name="Yoga Session",
            description="Relaxing yoga session.",
            instructor=self.instructor,
            facility=self.facility,
            start_time=now().replace(hour=10, minute=0, second=0),
            end_time=now().replace(hour=11, minute=0, second=0)
        )

        # Create bookings for attendance tracking
        self.booking_attended = Booking.objects.create(
            user=self.staff_user, gym_class=self.test_class, attended=True
        )
        self.booking_not_attended = Booking.objects.create(
            user=self.regular_user, gym_class=self.test_class, attended=False
        )

    def test_redirects_if_not_staff(self):
        """Test that non-staff users are redirected to the login page."""
        self.client.login(username="regular", password="TestPass123!")
        response = self.client.get(self.manage_classes_url)
        self.assertEqual(response.status_code, 302)

    def test_staff_can_access_manage_classes(self):
        """Test that staff can access the manage_classes view."""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(self.manage_classes_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/manage_classes.html")

    def test_classes_display_for_selected_date(self):
        """Test that only classes for the selected date are displayed."""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(
            self.manage_classes_url,
            {"date": self.class_date}
        )
        self.assertContains(response, "Yoga Session")
