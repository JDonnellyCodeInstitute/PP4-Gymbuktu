from django.test import TestCase
from classes.forms import ClassForm
from classes.models import Instructor, Facilitie, Class
from django.utils.timezone import now
from datetime import timedelta


class TestClassForm(TestCase):

    def setUp(self):
        """Set up an instructor and facility for testing."""
        self.instructor = Instructor.objects.create(name="John Doe")
        self.facility = Facilitie.objects.create(
            name="Studio",
            max_capacity=15
        )

    def test_form_is_valid(self):
        """Test that a fully valid form passes validation."""
        form_data = {
            "name": "Yoga Class",
            "description": "A relaxing yoga session.",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": (now() + timedelta(days=1)).isoformat(),
            "end_time": (now() + timedelta(days=1, hours=1)).isoformat(),
            "repeat_schedule": "weekly"
        }
        form = ClassForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Test that missing required fields make the form invalid."""
        valid_start_time = now()
        valid_end_time = valid_start_time + timedelta(hours=1)

        form = ClassForm({
            "name": "",
            "description": "",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": valid_start_time.isoformat(),
            "end_time": valid_end_time.isoformat(),
            "repeat_schedule": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("description", form.errors)

    def test_end_time_must_be_after_start_time(self):
        """Test that a class cannot have start_time >= end_time."""
        form_data = {
            "name": "Yoga Class",
            "description": "A relaxing yoga session.",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": (now() + timedelta(days=1, hours=1)).isoformat(),
            "end_time": (now() + timedelta(days=1)).isoformat(),
            "repeat_schedule": "weekly"
        }
        form = ClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn(
            "The class start must be before the end.", form.errors["__all__"]
        )

    def test_invalid_repeat_schedule(self):
        """Test that an invalid repeat_schedule value is rejected."""
        form_data = {
            "name": "Yoga Class",
            "description": "A relaxing yoga session.",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": (now() + timedelta(days=1)).isoformat(),
            "end_time": (now() + timedelta(days=1, hours=1)).isoformat(),
            "repeat_schedule": "monthly"  # Not in valid choices
        }
        form = ClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("repeat_schedule", form.errors)

    def test_blank_repeat_schedule_is_valid(self):
        """Test that leaving repeat_schedule blank is valid."""
        form_data = {
            "name": "Yoga Class",
            "description": "A relaxing yoga session.",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": (now() + timedelta(days=1)).isoformat(),
            "end_time": (now() + timedelta(days=1, hours=1)).isoformat(),
            "repeat_schedule": ""  # Optional field
        }
        form = ClassForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_conflicting_schedule_with_same_facility(self):
        """Test that a class with overlapping
        time and same facility is rejected."""
        start_time = now() + timedelta(days=1, hours=1)
        end_time = start_time + timedelta(hours=1)

        # Create a different instructor
        another_instructor = Instructor.objects.create(name="Jane Doe")

        # Create an existing class in the facility
        Class.objects.create(
            name="Existing Class",
            description="Test class",
            instructor=another_instructor,
            facility=self.facility,
            start_time=start_time,
            end_time=end_time,
        )

        # Create a conflicting class in the same facility
        new_class = ClassForm(data={
            "name": "Conflicting Class",
            "description": "Test conflict",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": start_time,
            "end_time": end_time,
        })

        self.assertFalse(new_class.is_valid())

        # Check non-field error
        self.assertIn("__all__", new_class.errors)
        self.assertIn(
            f"{self.facility.name} is hosting a class at this time.",
            new_class.errors["__all__"]
        )

    def test_conflicting_schedule_with_same_instructor(self):
        """Test that an instructor cannot be booked for overlapping classes."""
        start_time = now() + timedelta(days=1, hours=1)
        end_time = start_time + timedelta(hours=1)

        # Create an existing class for the instructor
        Class.objects.create(
            name="Existing Class",
            description="Test class",
            instructor=self.instructor,
            facility=self.facility,
            start_time=start_time,
            end_time=end_time,
        )

        # Create a conflicting class with the same instructor
        new_class = ClassForm(data={
            "name": "Conflicting Class",
            "description": "Test conflict",
            "instructor": self.instructor.id,
            "facility": self.facility.id,
            "start_time": start_time,
            "end_time": end_time,
        })

        self.assertFalse(new_class.is_valid())

        # Check non-field error
        self.assertIn("__all__", new_class.errors)
        self.assertIn(
            f"{self.instructor.name} is teaching a class at this time.",
            new_class.errors["__all__"]
        )
