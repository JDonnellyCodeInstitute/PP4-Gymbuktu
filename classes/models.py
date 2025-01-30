from django.db import models
from django.contrib.auth.models import User
from facilities.models import Facilitie

CLASS_STATUS = ((0, "Confirmed"), (1, "Cancelled"), (2, "Completed"))

class Class(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    instructor = models.CharField(max_length=20)
    facility = models.ForeignKey(
        Facilitie,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    capacity = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.instructor} at {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        if not self.capacity:
            self.capacity = self.facility.max_capacity
        super().save(*args, **kwargs)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(Class, on_delete=models.CASCADE)   
    # Status of the booking (e.g., confirmed, cancelled)
    class_status = models.IntegerField(choices=CLASS_STATUS, default=0)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.gym_class.name} ({self.self.get_class_status_display()})"
