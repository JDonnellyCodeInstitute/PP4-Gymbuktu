from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from facilities.models import Facilitie

CLASS_STATUS = ((0, "Confirmed"), (1, "Cancelled"), (2, "Completed"))


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def available_slots(self):
        """Returns the number of available slots
        based on the facility's max capacity."""
        booked_slots = self.bookings.filter(class_status=0).count()
        return max(self.facility.max_capacity - booked_slots, 0)

    def mark_completed(self):
        """Marks the class as completed if it has ended."""
        if self.end_time < timezone.now():
            self.bookings.filter(class_status=0).update(class_status=2)

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

    def __str__(self):
        return (
            f"{self.user.username} - {self.gym_class.name} "
            f"({self.get_class_status_display()})"
        )
