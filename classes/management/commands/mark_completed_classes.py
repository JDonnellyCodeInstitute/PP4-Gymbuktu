from django.core.management.base import BaseCommand
from classes.models import Class
from django.utils import timezone


class Command(BaseCommand):
    help = "Mark classes as completed if their end time has passed."

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Get all classes that have ended and are marked as confirmed
        completed_classes = Class.objects.filter(
            end_time__lt=now,
            class_status=0
        )

        # Update status
        updated_count = 0
        for gym_class in completed_classes:
            gym_class.class_status = 2
            gym_class.save()
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{updated_count} classes completed.")
        )
