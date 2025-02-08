from django.core.management.base import BaseCommand
from classes.models import Class
from django.utils import timezone


class Command(BaseCommand):
    help = "Mark classes as completed if their end time has passed."

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Get all classes that have ended but are not marked as completed
        completed_classes = Class.objects.filter(
            end_time__lt=now
        )

        # Update status
        updated_count = 0
        for gym_class in completed_classes:
            gym_class.status = 2
            gym_class.save()
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{updated_count} classes completed.")
        )
