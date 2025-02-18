from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from classes.forms import ClassForm
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

    def test_invalid_date_defaults_to_today(self):
        """Test that an invalid date will default to today"""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(
            self.manage_classes_url,
            {"date": "Invalid-date"}
        )
        # Test class still shows
        self.assertContains(response, "Yoga Session")

    def test_attendance_data_in_context(self):
        """Test that attendance data is passed correctly in the context."""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(self.manage_classes_url)
        context = response.context

        self.assertIn("class_data", context)
        self.assertEqual(len(context["class_data"]), 1)
        self.assertEqual(context["class_data"][0]["total_bookings"], 2)
        self.assertEqual(context["class_data"][0]["attended_count"], 1)


class TestManageAttendanceView(TestCase):

    def setUp(self):
        """Set up test users, classes, and bookings."""
        self.client = Client()

        # Create a staff user
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staffuser@gmail.com",
            password="TestPass123!",
            is_staff=True
        )

        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="TestPass123!"
        )

        # Create an instructor
        self.instructor = Instructor.objects.create(name="John Doe")

        # Create a facility
        self.facility = Facilitie.objects.create(
            name="Studio",
            max_capacity=10
        )

        # Create a class (future-dated to avoid conflicts)
        start_time = now() + timedelta(days=1, hours=10)
        end_time = start_time + timedelta(hours=1)

        self.gym_class = Class.objects.create(
            name="Yoga Session",
            description="Relaxing yoga class",
            instructor=self.instructor,
            facility=self.facility,
            start_time=start_time,
            end_time=end_time
        )

        # Create bookings
        self.booking1 = Booking.objects.create(
            user=self.user, gym_class=self.gym_class, class_status=0
        )
        self.booking2 = Booking.objects.create(
            user=self.staff_user, gym_class=self.gym_class, class_status=0
        )

        # Set the URL for managing attendance
        self.manage_attendance_url = reverse(
            "manage_attendance", args=[self.gym_class.id]
        )

    def test_redirect_if_not_logged_in(self):
        """Ensure unauthenticated users are redirected to login."""
        response = self.client.get(self.manage_attendance_url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.manage_attendance_url}"
        )

    def test_redirect_non_staff(self):
        """Ensure non-staff users cannot access the manage attendance page."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(self.manage_attendance_url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.manage_attendance_url}"
        )

    def test_staff_can_access_manage_attendance(self):
        """Ensure staff users can access the manage attendance page."""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(self.manage_attendance_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/manage_attendance.html")
        self.assertIn("gym_class", response.context)
        self.assertIn("bookings", response.context)
        self.assertEqual(response.context["total_bookings"], 2)

    def test_attendance_updates_correctly(self):
        """Ensure attendance updates correctly
        when staff marks users as attended."""
        self.client.login(username="staffuser", password="TestPass123!")

        # Mark first user as attended
        post_data = {
            f"attended_{self.booking1.id}": "on",
        }

        response = self.client.post(
            self.manage_attendance_url,
            post_data,
            follow=True
        )

        # Refresh booking instances
        self.booking1.refresh_from_db()
        self.booking2.refresh_from_db()

        # Verify updates
        self.assertTrue(self.booking1.attended)  # First user marked attended
        self.assertFalse(self.booking2.attended)  # Second user remains absent

        # Check class's attendees list is updated
        self.gym_class.refresh_from_db()
        self.assertIn(self.booking1.user, self.gym_class.attendees.all())
        self.assertNotIn(self.booking2.user, self.gym_class.attendees.all())

        # Verify success message
        messages = list(response.context["messages"])
        self.assertTrue(any(
            "Attendance updated successfully!" in msg.message
            for msg in messages
        ))

        # Ensure redirection back to manage attendance page
        self.assertRedirects(response, self.manage_attendance_url)


class TestAddClassView(TestCase):

    def setUp(self):
        """Set up test data, including a staff user and required models."""
        # Create a staff user
        self.staff_user = User.objects.create_user(
            username="staffuser", password="TestPass123!", is_staff=True
        )

        # Create a non-staff user
        self.non_staff_user = User.objects.create_user(
            username="testuser", password="TestPass123!"
        )

        # Create an instructor and a facility
        self.instructor = Instructor.objects.create(name="John Doe")
        self.facility = Facilitie.objects.create(
            name="Studio",
            max_capacity=15
        )

        # Define the URL for adding a class
        self.add_class_url = reverse("add_class")

    def test_staff_can_access_add_class_page(self):
        """Ensure staff users can access the add class form."""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(self.add_class_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/class_form.html")
        self.assertIsInstance(response.context["form"], ClassForm)

    def test_non_staff_redirected_from_add_class_page(self):
        """Ensure non-staff users are redirected
        when trying to access add class."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(self.add_class_url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.add_class_url}"
        )

    def test_staff_can_add_class(self):
        """Ensure staff users can successfully add a class."""
        self.client.login(username="staffuser", password="TestPass123!")
        form_data = {
            "name": "Yoga Class",
            "description": "A relaxing yoga session.",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": "2025-12-01T10:00",
            "end_time": "2025-12-01T11:00",
            "repeat_schedule": "weekly"
        }
        response = self.client.post(self.add_class_url, form_data, follow=True)

        # Verify class was created
        self.assertEqual(Class.objects.count(), 1)
        new_class = Class.objects.first()
        self.assertEqual(new_class.name, "Yoga Class")

        # Verify redirect and success message
        self.assertRedirects(response, reverse("manage_classes"))
        messages = list(response.context["messages"])
        self.assertTrue(any(
            "Class added successfully!" in msg.message for msg in messages
        ))

    def test_invalid_form_submission_fails(self):
        """Ensure an invalid form submission does not create a class."""
        self.client.login(username="staffuser", password="TestPass123!")
        form_data = {
            "name": "",  # Name is required
            "description": "Missing required fields test",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": "2025-12-01T10:00",
            "end_time": "2025-12-01T09:00",  # End time before start time
            "repeat_schedule": "weekly"
        }
        response = self.client.post(self.add_class_url, form_data)

        # Verify class was NOT created
        self.assertEqual(Class.objects.count(), 0)

        # Ensure form contains errors
        self.assertFormError(
            response, "form", "name", "This field is required."
        )
        self.assertFormError(
            response, "form", None, "The class start must be before the end."
        )


class TestEditClassView(TestCase):

    def setUp(self):
        """Set up test data, including a staff
        user, class, and required models."""
        # Create a staff user
        self.staff_user = User.objects.create_user(
            username="staffuser", password="TestPass123!", is_staff=True
        )

        # Create a non-staff user
        self.non_staff_user = User.objects.create_user(
            username="testuser", password="TestPass123!"
        )

        # Create an instructor and a facility
        self.instructor = Instructor.objects.create(name="John Doe")
        self.facility = Facilitie.objects.create(
            name="Studio", max_capacity=15
        )

        # Create a test class
        self.test_class = Class.objects.create(
            name="Yoga Class",
            description="A relaxing yoga session.",
            instructor=self.instructor,
            facility=self.facility,
            start_time="2025-12-01T10:00",
            end_time="2025-12-01T11:00",
            repeat_schedule="weekly"
        )

        # Define the URL for editing the class
        self.edit_class_url = reverse("edit_class", args=[self.test_class.id])

    def test_staff_can_access_edit_class_page(self):
        """Ensure staff users can access the edit class form."""
        self.client.login(username="staffuser", password="TestPass123!")
        response = self.client.get(self.edit_class_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/class_form.html")
        self.assertIsInstance(response.context["form"], ClassForm)
        self.assertEqual(response.context["form"].instance, self.test_class)

    def test_non_staff_redirected_from_edit_class_page(self):
        """Ensure non-staff users are redirected
        when trying to access edit class."""
        self.client.login(username="testuser", password="TestPass123!")
        response = self.client.get(self.edit_class_url)
        self.assertRedirects(
            response, f"{reverse('login')}?next={self.edit_class_url}"
        )

    def test_staff_can_edit_class(self):
        """Ensure staff users can successfully edit a class."""
        self.client.login(username="staffuser", password="TestPass123!")
        form_data = {
            "name": "Updated Yoga Class",
            "description": "An updated relaxing yoga session.",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": "2025-12-01T12:00",
            "end_time": "2025-12-01T13:00",
            "repeat_schedule": "daily"
        }
        response = self.client.post(
            self.edit_class_url, form_data, follow=True
        )

        # Verify class was updated
        self.test_class.refresh_from_db()
        self.assertEqual(self.test_class.name, "Updated Yoga Class")
        self.assertEqual(self.test_class.repeat_schedule, "daily")

        # Verify redirect and success message
        self.assertRedirects(response, reverse("manage_classes"))
        messages = list(response.context["messages"])
        self.assertTrue(any(
            "Class updated successfully!" in msg.message for msg in messages
        ))

    def test_invalid_form_submission_fails(self):
        """Ensure an invalid form submission does not update the class."""
        self.client.login(username="staffuser", password="TestPass123!")
        form_data = {
            "name": "",  # Name is required
            "description": "Missing required fields test",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": "2025-12-01T10:00",
            "end_time": "2025-12-01T09:00",  # End time before start time
            "repeat_schedule": "weekly"
        }
        response = self.client.post(self.edit_class_url, form_data)

        # Verify class was NOT updated
        self.test_class.refresh_from_db()
        self.assertNotEqual(
            self.test_class.description, "Missing required fields test"
        )

        # Ensure form contains errors
        self.assertFormError(
            response, "form", "name", "This field is required."
        )
        self.assertFormError(
            response, "form", None, "The class start must be before the end."
        )
