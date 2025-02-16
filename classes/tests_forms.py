from django.test import TestCase
from classes.forms import ClassForm
from classes.models import Instructor, Facilitie
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
