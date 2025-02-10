from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from facilities.models import Facilitie
from datetime import timedelta
from django.core.exceptions import ValidationError

CLASS_STATUS = ((0, "Confirmed"), (1, "Cancelled"), (2, "Completed"))

REPEAT_CHOICES = (
    (None, "Does Not Repeat"),
    ("daily", "Daily"),
    ("weekly", "Weekly"),
)


class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    facility = models.ForeignKey(
        Facilitie,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_status = models.IntegerField(choices=CLASS_STATUS, default=0)
    repeat_schedule = models.CharField(
        max_length=10,
        choices=REPEAT_CHOICES,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def available_slots(self):
        """Returns the number of available
        slots based on the facility's max capacity."""
        booked_slots = self.bookings.filter(class_status=0).count()
        return max(self.facility.max_capacity - booked_slots, 0)

    def mark_completed(self):
        """Marks the class as completed if it has ended."""
        if self.end_time < timezone.now():
            self.class_status = 2
            self.save()
            self.bookings.filter(class_status=0).update(class_status=2)

    def create_next_occurrence(self):
        """Creates the next occurrence of the class if it is set to repeat."""
        if self.repeat_schedule == "daily":
            new_start = self.start_time + timedelta(days=1)
            new_end = self.end_time + timedelta(days=1)
        elif self.repeat_schedule == "weekly":
            new_start = self.start_time + timedelta(weeks=1)
            new_end = self.end_time + timedelta(weeks=1)
        else:
            return None  # No repeat

        # Create new class instance
        return Class.objects.create(
            name=self.name,
            description=self.description,
            instructor=self.instructor,
            facility=self.facility,
            start_time=new_start,
            end_time=new_end,
            repeat_schedule=self.repeat_schedule
        )

    def clean(self):
        """Check for instructor and facility conflicts before saving."""
        overlapping_classes = Class.objects.filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)  # Exclude self to allow updates

        # Check instructor conflict
        if overlapping_classes.filter(instructor=self.instructor).exists():
            raise ValidationError(
                f"{self.instructor.name} is teaching a class at this time.")

        # Check facility conflict
        if overlapping_classes.filter(facility=self.facility).exists():
            raise ValidationError(
                f"{self.facility.name} is hosting a class at this time.")

    def save(self, *args, **kwargs):
        """Run validation before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.name} by {self.instructor.name} at "
            f"{self.start_time.strftime('%Y-%m-%d %H:%M')}"
        )

    class Meta:
        ordering = ['start_time']


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="bookings")
    class_status = models.IntegerField(choices=CLASS_STATUS, default=0)
    date = models.DateField(auto_now_add=True)

    def clean(self):
        """Ensure user is not double-booking overlapping classes."""
        overlapping_bookings = Booking.objects.filter(
            user=self.user,
            gym_class__start_time__lt=self.gym_class.end_time,
            gym_class__end_time__gt=self.gym_class.start_time,
            class_status=0
        ).exclude(id=self.id)  # Exclude self for updates

        if overlapping_bookings.exists():
            raise ValidationError(
                "You are already booked for another class at this time.")

    def save(self, *args, **kwargs):
        """Run validation before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.username} - {self.gym_class.name} "
            f"({self.get_class_status_display()})"
        )
