from django.test import TestCase
from classes.forms import ClassForm
from classes.models import Instructor, Facilitie
from django.utils.timezone import now, timedelta


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
