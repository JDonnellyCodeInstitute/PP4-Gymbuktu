from django.db import models


class Facilitie(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    max_capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
